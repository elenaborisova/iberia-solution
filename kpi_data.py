import requests

months_names = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}


# Helper functions
def extract_priority(items):
    values_low = [item['incidences_number'] for item in items if item['priority'] == 'Baja']
    values_medium = [item['incidences_number'] for item in items if item['priority'] == 'Media']
    values_high = [item['incidences_number'] for item in items if item['priority'] == 'Alta']
    values_critical = [item['incidences_number'] for item in items if item['priority'] == 'Crítica']
    return values_low, values_medium, values_high, values_critical


def get_res_time_percentage1(items):
    total_low = values_low = 0
    total_medium = values_medium = 0

    for item in items:
        if item['priority'] == 'Baja':
            if item['date_diff'] < 15:
                values_low += item['count']
            total_low += item['count']
        else:
            if item['date_diff'] < 5:
                values_medium += item['count']
            total_medium += item['count']

    return int(values_low / total_low * 100), int(values_medium / total_medium * 100)


def get_res_time_percentage2(items):
    total_high = values_high = 0
    total_critical = values_critical = 0

    for item in items:
        if item['priority'] == 'Alta':
            diff = int(item['res_time'].split(':')[1]) - int(item['create_time'].split(':')[1])
            if diff < 8:
                values_high += item['count']
            total_high += item['count']
        else:
            diff = int(item['res_time'].split(':')[1]) - int(item['create_time'].split(':')[1])
            if diff < 4:
                values_critical += item['count']
            total_critical += item['count']

    return int(values_high / total_high * 100), int(values_critical / total_critical * 100)


# 1. Total number of critical incidents (P1) of the month
def get_total_number_of_critical_incidents():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi1/incvol/'
    data_json = requests.get(url).json()

    labels = [months_names[item['month']] for item in data_json['items']]
    values = [item['incidences_number'] for item in data_json['items']]

    return labels, values


# 2. Number of incidents raised per priority in the month
def get_total_number_of_incidents_per_priority():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi2/incvol/'
    data_json = requests.get(url).json()

    months = sorted(list(set([item['month'] for item in data_json['items']])))
    months_labels = [months_names[m] for m in months]
    values_low, values_medium, values_high, values_critical = extract_priority(data_json['items'])

    return months_labels, values_low, values_medium, values_high, values_critical


# 3. Total number of incidents raised in the month
def get_total_number_of_incidents():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi3/incvol/'
    data_json = requests.get(url).json()

    labels = [months_names[item['month']] for item in data_json['items']]
    values = [item['incidences_number'] for item in data_json['items']]

    return labels, values


# 4. Number of incidents in the backlog per priority in the month
def get_number_of_incidents_backlog_per_priority():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi4/incvol/'
    data_json = requests.get(url).json()

    months = sorted(list(set([item['month'] for item in data_json['items']])))
    months_labels = [months_names[m] for m in months]
    values_low, values_medium, values_high, values_critical = extract_priority(data_json['items'])

    return months_labels, values_low, values_medium, values_high, values_critical


# 5. Number of incidents per cause
def get_number_of_incidents_per_cause():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi5/incvol/'
    data_json = requests.get(url).json()

    labels = [item['type'] for item in data_json['items']]
    values = [item['count'] for item in data_json['items']]

    return labels, values


# 6. Number of incidents per status
def get_number_of_incidents_per_status():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi6/incvol/'
    data_json = requests.get(url).json()

    labels = [item['type'] for item in data_json['items']]
    values = [item['count'] for item in data_json['items']]

    return labels, values


# 7. Number of incidents per customer company group
def get_number_of_incidents_per_company_group():
    url = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi7/incvol/'
    data_json = requests.get(url).json()

    labels = [item['comp_group'] for item in data_json['items']]
    values = [item['count'] for item in data_json['items']]

    return labels, values


# 8. Number of incidents P1 in the month meeting SLA resolution time
def get_percentage_of_incidents_meeting_sla():
    url_day_diff = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi8/incvol/'
    data_json = requests.get(url_day_diff).json()

    url_time_diff = 'https://g5cb9edca1cffa5-iberiadb.adb.eu-milan-1.oraclecloudapps.com/ords/tip/kpi9/incvol/'
    data_json2 = requests.get(url_time_diff).json()

    percentage_low, percentage_medium = get_res_time_percentage1(data_json['items'])
    percentage_high, percentage_critical = get_res_time_percentage2(data_json2['items'])

    return percentage_low, percentage_medium, percentage_high, percentage_critical
