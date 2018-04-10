#!/usr/bin/env python

import unicodecsv
import sys
import codecs

FIELDNAMES = 'project_identifier,amendment_number,amendment_date,agreement_type,recipient_type,recipient_business_number,recipient_legal_name,recipient_operating_name_en,recipient_operating_name_fr,research_organization_name_en,research_organization_name_fr,recipient_country,recipient_province,recipient_city_en,recipient_city_fr,recipient_postal_code,federal_riding_name_en,federal_riding_name_fr,federal_riding_number,prog_name_en,prog_name_fr,prog_purpose_en,prog_purpose_fr,agreement_title_en,agreement_title_fr,agreement_number,agreement_value,foreign_currency_type,foreign_currency_value,agreement_start_date,agreement_end_date,coverage_en,coverage_fr,description_en,description_fr,naics_identifier,expected_results_en,expected_results_fr,additional_information_en,additional_information_fr,owner_org,owner_org_title'.split(',')

assert sys.stdin.read(3) == codecs.BOM_UTF8

in_csv = unicodecsv.DictReader(sys.stdin, encoding='utf-8')
out_csv = unicodecsv.DictWriter(sys.stdout, fieldnames=FIELDNAMES, encoding='utf-8')
out_csv.writeheader()

for line in in_csv:
    line['project_identifier'] = line.pop('ref_number')
    line['agreement_type'] = line.pop('type')
    r_en = line.pop('recipient_name_en')
    r_fr = line.pop('recipient_name_fr')
    if r_en == r_fr:
        line['recipient_legal_name'] = r_en
    else:
        line['recipient_legal_name'] = r_en + '\t' + r_fr
    line['recipient_city_en'] = line.pop('recipient_region_en')
    line['recipient_city_fr'] = line.pop('recipient_region_fr')
    line['prog_purpose_en'] = line.pop('purpose_en')
    line['prog_purpose_fr'] = line.pop('purpose_fr')
    line['agreement_title_en'] = line.pop('proj_name_en')
    line['agreement_title_fr'] = line.pop('proj_name_fr')
    line['agreement_number'] = (
        line.pop('prog_number') + '\t' + line.pop('proj_number')).strip()
    line['agreement_value'] = line.pop('value')
    line['agreement_start_date'] = line.pop('date')
    line['additional_information_en'] = (
        line.pop('comments_en') + '\t' + line.pop('additional_info_en')).strip()
    line['additional_information_fr'] = (
        line.pop('comments_fr') + '\t' + line.pop('additional_info_fr')).strip()
    out_csv.writerow(line)
