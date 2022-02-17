import json
import requests
import datetime
import re


class Scraper:
    @staticmethod
    def scrape():
        url = 'https://joinposter.com/crm/login'
        data_url = 'https://joinposter.com/listings/crm_clients/data'
        data = {
            'email': 'Lavalet861@gmail.com',
            'password': '23002a02c47',
            'select[]': ['action_date', 'id_client', 'client_number', 'url', 'company_name', 'status_type', 'name',
                         'country', 'date_reg', 'date_pay', 'first_payment_date'],
        }
        session = requests.Session()
        session.post(url, data=data, headers=dict(Referer=url))
        select = session.post(data_url, data=data, headers=dict(Referer=url))
        clients_data = json.loads(select.text)
        return clients_data


class Sorter:
    def _get_date(self):
        pass

    def _is_out_of_payment(self):
        if self is None:
            return False
        x = re.split(r'[-| ]', str(self))
        x_day = datetime.date(int(x[0]), int(x[1]), int(x[2]))
        if x_day < datetime.date.today():
            return True

    def _is_out_of_test(self):
        if self is None:
            return False
        x = re.split(r'[-| ]', str(self))
        x_day = datetime.date(int(x[0]), int(x[1]), int(x[2]))
        if x_day < (datetime.date.today() + datetime.timedelta(days=5)):
            return True

    def _is_in_month(self):
        if self is None:
            return False
        x = re.split(r'[-| ]', str(self))
        today = datetime.date.today()
        if today.year == int(x[0]) and today.month == int(x[1]):
            return True

    def _is_today(self):
        if self is None:
            return False
        x = re.split(r'[-| ]', str(self))
        today = datetime.date.today()
        if today.year == int(x[0]) and today.month == int(x[1]) and today.day == int(x[2]):
            return True

    def sort(self):
        count_of_payed = 0
        count_of_hot = 0
        count_of_cold = 0
        count_of_payed_in_month = 0
        count_of_registration_today = 0
        count_of_registration_month = 0
        expires_of_payment = []
        expires_of_test = []

        for i in range(self['data_count']):
            if self['data'][i]['status_type']['value'] == 2 or self['data'][i]['status_type']['value'] == 16:
                count_of_payed += 1
                if Sorter._is_in_month(self['data'][i]['first_payment_date']):
                    count_of_payed_in_month += 1
                if Sorter._is_in_month(self['data'][i]['date_reg']):
                    count_of_registration_month += 1
                if Sorter._is_out_of_payment(self['data'][i]['date_pay']['value']):
                    expires_of_payment.append({
                        'id': self['data'][i]['id_client']['value'],
                        'url': self['data'][i]['url'],
                        'company_name': self['data'][i]['company_name'],
                        'status': self['data'][i]['status_type']['value'],
                        'date_pay': self['data'][i]['date_pay']['value'],
                    })
            if self['data'][i]['status_type']['value'] == 1:
                count_of_hot += 1
                if Sorter._is_in_month(self['data'][i]['date_reg']):
                    count_of_registration_month += 1
                if Sorter._is_today(self['data'][i]['date_reg']):
                    count_of_registration_today += 1
                if Sorter._is_out_of_test(self['data'][i]['date_pay']['value']):
                    expires_of_test.append({
                        'id': self['data'][i]['id_client']['value'],
                        'url': self['data'][i]['url'],
                        'company_name': self['data'][i]['company_name'],
                        'status': self['data'][i]['status_type']['value'],
                        'date_pay': self['data'][i]['date_pay']['value'],
                    })

            if self['data'][i]['status_type']['value'] == 8:
                count_of_cold += 1
                if Sorter._is_in_month(self['data'][i]['date_reg']):
                    count_of_registration_month += 1
                if Sorter._is_today(self['data'][i]['date_reg']):
                    count_of_registration_today += 1
            if self['data'][i]['status_type']['value'] == 18 or self['data'][i]['status_type']['value'] == 19:
                if Sorter._is_in_month(self['data'][i]['date_reg']):
                    count_of_registration_month += 1
                if Sorter._is_today(self['data'][i]['date_reg']):
                    count_of_registration_today += 1

        counts = {
            'count_of_payed': count_of_payed,
            'count_of_hot': count_of_hot,
            'count_of_cold': count_of_cold,
            'count_of_payed_in_month': count_of_payed_in_month,
            'count_of_registration_in_month': count_of_registration_month,
            'count_of_registration_today': count_of_registration_today,
            'expires_of_payment': expires_of_payment,
            'expires_of_test': expires_of_test,
        }

        return counts


def get_sorted_list():
    return Sorter.sort(Scraper.scrape())
