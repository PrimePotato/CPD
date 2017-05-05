
import re
import pandas as pd
from db_flask.manage import Disposal, db
import email_service
from scraper import regex_dict, extract_field
from datetime import datetime as dt
from geopy.geocoders import Nominatim
import geocoder as gcd
import time

import locale
locale.setlocale(locale.LC_ALL, 'uk')
geo = Nominatim()
esx = email_service.Extractor('robert.cooper@peppercorn.london', 'C0ntent123qwerty')


def extract_postcode(s):
    try:
        rgx = re.search('[a-zA-Z]{1,2}\d{1,2}([a-zA-Z])?(\s)?\d{1,2}[a-zA-Z]{2}', s)
        return rgx.group()
    except Exception:
        print('Extract post code issue {}'.format(s))
        s.replace('O', '0')
        try:
            rgx = re.search('[a-zA-Z]{1,2}\d{1,2}([a-zA-Z])?(\s)?\d{1,2}[a-zA-Z]{2}', s)
            return rgx.group()
        except Exception:
            return None
        return None


def extract_areacode(s):
    try:
        rgx = re.search('[a-zA-Z]{1,2}\d{1,2}[a-zA-Z]?', s)
        return rgx.group()
    except Exception:
        print('Extract area code issue {}'.format(s))
        return None


def _clean_extract(s):
    if isinstance(s, str):
        try:
            d = locale.atof(s)
            return d
        except Exception:
            return s.replace('\\r\\n', '').replace('\\xe2\\x80\\x93', '-').replace('\\x96', '-').lstrip().rstrip()


def geocode_dic(loc, pc, ac):
    time.sleep(0.5)
    gg = gcd.google(loc + ', London')
    while gg.status != 'ZERO_RESULTS':
        print(gg.status)
        if gg.status is 'OK':
            if not pc:
                pc = gg.postal
            return {
                'address': gg.address,
                'lng': gg.lng,
                'lat': gg.lat,
                'post_code': pc,
                'area_code': ac}
        if gg.status is 'OVER_QUERY_LIMIT':
            break
    if pc is not loc and pc is not None:
        return geocode_dic(pc, pc, ac)
    if ac is not loc and ac is not None:
        return geocode_dic(ac, pc, ac)
    return {'address': None,
            'lng': None,
            'lat': None,
            'post_code': None,
            'area_code': None}


def update_database():

    print('***Fetching Email***')
    mbs = esx.message_bodies()
    for k, m in mbs.items():
        # print('--- Processing Email with UID {}'.format(k) + '-------------------------------------------------')
        listing_type = determine_listing_type(m)
        if listing_type == 'Acquisition':
            pass
            # rpt = upload_acquisition(m)
            # if not rpt:
            #     print('!!! Upload failed for UID {} !!!'.format(k))
            #     continue
        elif listing_type == 'Disposal':
            rpt = upload_disposal(m, k)
            if rpt:
                print('Database updated with UID {}'.format(k))
            else:
                pass


def determine_listing_type(msg):
    if extract_field(('New disposal posted!', 0), msg):  # is not None:
        return 'Disposal'
    elif extract_field(('New acquisition posted!', 0), msg):  # is not None:
        return 'Acquisition'
    else:
        return 'Unrecognised'


def upload_acquisition(msg):
    efs = {f: (extract_field(v, msg)) for f, v in regex_dict.items()}

    if not efs['location']:
        return False

    return True


def upload_disposal(msg, uid):
    efs = {f: (extract_field(v, msg)) for f, v in regex_dict.items()}

    if not efs['location']:
        return False

    cfs = {f: _clean_extract(v) for f, v in efs.items()}

    pc = extract_postcode(cfs['location'])
    if pc:
        ac = extract_areacode(pc)
    else:
        ac = extract_areacode(cfs['location'])
    gd = geocode_dic(cfs['location'], pc, ac)

    cfs['date_posted'] = dt.strptime(cfs['date_posted'], '%d/%m/%Y')
    try:
        ex = {'size_avg': (cfs['size_min'] + cfs['size_max']) / 2}
    except Exception:
        ex = {'size_avg': None}

    rld = {'email_id': int(uid), **cfs, **ex, **gd}

    l = Disposal(**rld)
    db.session.add(l)
    db.session.commit()
    return True


def del_all():
    Disposal.query.delete()


def all_data():
    qry = db.session.query(Disposal).all()
    d = pd.DataFrame([l.to_dict() for l in qry])
    d.index.name = 'id'
    return d

del_all()
update_database()