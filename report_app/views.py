from django import template

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect

from django.template import loader

from django.urls import reverse

import json

from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User
import csv

import os

from .models import Report
import pymssql




def get_connection():

    conn = pymssql.connect(server = '192.168.5.79', user = 'chatboat_sa', password = 'ch@tb0@t$@', database = 'zu_chatbot_log_dev')



    return conn





def get_repeated_bot_users():

    busy_count = []



    try:

        connection = get_connection()

        cursor = connection.cursor()

        SQL_select_Query = 'SELECT * from dbo.repeated_bot_users_day_view order by ev_count desc;'
        cursor.execute(SQL_select_Query)

        busy_count = cursor.fetchall()

    except pymssql.Error as error:

        print("Error while fetching data from SQL server", error)



    finally:

        if connection:

            cursor.close()

            connection.close()

            # print("SQL connection is closed")

    return busy_count





def get_repeated_bot_monthly_users():

    busy_count = []

    try:

        connection = get_connection()

        cursor = connection.cursor()

        SQL_select_Query = 'SELECT * from dbo.repeated_bot_users_monthly_view order by ev_count desc;'
        cursor.execute(SQL_select_Query)

        busy_count = cursor.fetchall()

    except pymssql.Error as error:

        print("Error while fetching data from SQL server", error)



    finally:

        if connection:

            cursor.close()

            connection.close()

            # print("SQL connection is closed")

    return busy_count





def get_busy_period_count():

    busy_count = []

    try:

        connection = get_connection()

        cursor = connection.cursor()

        SQL_select_Query = 'SELECT * from dbo.busy_period_count order by intent_counts desc;'
        cursor.execute(SQL_select_Query)

        busy_count = cursor.fetchall()

    except pymssql.Error as error:

        print("Error while fetching data from SQL server", error)



    finally:

        if connection:

            cursor.close()

            connection.close()

            # print("SQL connection is closed")

    return busy_count





def get_busy_period_count_monthly():

    busy_count_month = []

    try:

        connection = get_connection()

        cursor = connection.cursor()

        SQL_select_Query = 'SELECT * from dbo.busy_period_count_monthly order by intent_counts desc;'
        cursor.execute(SQL_select_Query)

        busy_count_month = cursor.fetchall()

    except pymssql.Error as error:

        print("Error while fetching data from SQL server", error)



    finally:

        if connection:

            cursor.close()

            connection.close()

            # print("SQL connection is closed")

    return busy_count_month


def live_count():
    live = []
    live_month = []

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor1 = connection.cursor()

        SQL_select_Query = 'Select Top 1 * from dbo.livechat_daywise order by day desc;'
        cursor.execute(SQL_select_Query)

        live = cursor.fetchall()
        SQL_select_Query1 = 'Select top 1 * from dbo.livechat_monthwise order by month desc;'
        cursor1.execute(SQL_select_Query1)

        live_month = cursor1.fetchall()

    except pymssql.Error as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return live, live_month



def reset_count():

    reset_count = []

    reset_month = []

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor1 = connection.cursor()

        SQL_select_Query = 'Select Top 1 * from dbo.reset_daywise order by day desc;'
        cursor.execute(SQL_select_Query)

        reset_count = cursor.fetchall()

        print("reset_count", reset_count)



        SQL_select_Query1 = 'Select top 1 * from dbo.reset_monthwise order by month desc;'
        cursor1.execute(SQL_select_Query1)

        reset_month = cursor1.fetchall()

        print("reset_month", reset_month)

    except pymssql.Error as error:

        print("Error while fetching data from SQL server", error)



    finally:

        if connection:

            cursor.close()

            connection.close()

            print("SQL connection is closed")

    return reset_count, reset_month





def get_total_users_cnt():

    total_eng_users_cnt = 0

    total_new_users_cnt = 0

    """ query data from the log_record table """

    try:

        connection = get_connection()

        cursor2 = connection.cursor()

        cursor1 = connection.cursor()



        # postgreSQL_select_Query = 'SELECT * from chatbot.total_cnt_view_mview;'

        eng_select_Query = 'SELECT * from dbo.engaged_users_view1;'

        cursor2.execute(eng_select_Query)

        new_select_Query = 'SELECT * from dbo.new_users_view1;'

        cursor1.execute(new_select_Query)

        # log_record = cursor.fetchone()

        total_eng_users_cnt = cursor2.fetchall()

        total_new_users_cnt = cursor1.fetchall()

        # print("---> ", total_eng_users_cnt)

        # print("---> ", total_new_users_cnt)

        # total_users_cnt = [list(tp) for tp in desc_total_cnt]



    except pymssql.Error as error:

        print("Error while fetching total_desc_cnt from SQL", error)



    finally:

        # closing database connection.

        if connection:

            cursor2.close()

            cursor1.close()

            connection.close()

            print("SQL connection is closed")



    return total_eng_users_cnt, total_new_users_cnt





def get_monthly_data():

    list_log_record = ''

    """ query data from the log_record table """

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor1 = connection.cursor()

        cursor2 = connection.cursor()



        select_Query = 'SELECT * from dbo.monthly_data_view;'
        cursor.execute(select_Query)

        log_record = cursor.fetchall()

        eng_select_Query = 'SELECT * from dbo.monthly_engaged_users_view;'
        cursor1.execute(eng_select_Query)

        engaged_u = cursor1.fetchall()



        new_select_Query = 'SELECT * from dbo.monthly_new_users_view;'
        cursor2.execute(new_select_Query)

        new_u = cursor2.fetchall()

        list_log_record = [list(tp) for tp in log_record]



    except pymssql.Error as error:

        print("Error while fetching data from PostgreSQL", error)



    finally:

        if connection:

            cursor.close()

            connection.close()

    return list_log_record, engaged_u, new_u





def get_daily_data():

    engaged_u = 0

    new_u = 0

    list_log_record = ''

    """ query data from the log_record table """

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor1 = connection.cursor()

        cursor2 = connection.cursor()



        postgreSQL_select_Query = 'SELECT * from dbo.daily_data_view;'
        cursor.execute(postgreSQL_select_Query)
        log_record = cursor.fetchall()

        eng_select_Query = 'SELECT * from dbo.engaged_users_view1;'
        cursor1.execute(eng_select_Query)

        engaged_u = cursor1.fetchall()



        new_select_Query = 'SELECT * from dbo.new_users_view1;'
        cursor2.execute(new_select_Query)
        
        new_u = cursor2.fetchall()

        # cursor2.execute(new_select_Query)

        # engaged_u = cursor1.fetchall()

        # new_u = cursor2.fetchall()

        # print("Selecting rows from chatbot_log table using cursor.fetchall")

        # log_record = cursor.fetchone()

        # log_record = cursor.fetchall()

        list_log_record = [list(tp) for tp in log_record]

    except pymssql.Error as error:

        print("Error while fetching data from SQL", error)



    finally:

        # closing database connection.

        if connection:

            cursor.close()

            connection.close()

            print("SQL connection is closed")



    # engaged_u, new_u =  get_total_users_cnt()

    return list_log_record, engaged_u, new_u





def get_total_event_cnt():

    global total_desc_cnt

    """ query data from the log_record table """



    try:

        connection = get_connection()

        cursor = connection.cursor()



        # postgreSQL_select_Query = 'SELECT * from chatbot.total_cnt_view_mview;'

        select_Query = 'SELECT * from dbo.total_ans_cnt_view;'

        cursor.execute(select_Query)

        # print("Selecting rows from chatbot_log table using cursor.fetchall")

        # log_record = cursor.fetchone()

        desc_total_cnt = cursor.fetchall()

        total_desc_cnt = [list(tp) for tp in desc_total_cnt]



    except pymssql.Error as error:

        print("Error while fetching total_desc_cnt from PostgreSQL", error)



    finally:

        # closing database connection.

        if connection:

            cursor.close()

            connection.close()

            print("PostgreSQL connection is closed")



    return total_desc_cnt





def getUserById(_userid):

    users = User.objects.get(id=_userid)

    # print(users)





def daily_charts():

    users_list = User.objects.filter(is_superuser=False)

    data, en, ne = get_daily_data()

    # total_eng_users = get_total_eng_users_cnt()

    pie_data = get_total_event_cnt()



    busy_count = get_busy_period_count()

    repeated_users = get_repeated_bot_users()

    reset, reset_month = reset_count()

    live, live_month = live_count()

    print("""==================================================================""")

    print("reset_month- > ", reset_month)

    print("reset", reset)



    event_categories = list()

    wrong_ans_data = list()

    right_ans_data = list()

    no_ans_data = list()



    for dt in data:

        if dt[1].__str__() not in event_categories:

            event_categories.append(dt[1].__str__())  # for answer desc



    edict = {}

    for i in event_categories:

        temp = [0, 0, 0]

        if i not in edict.keys():

            for dt in data:

                if i == dt[1].__str__():

                    if dt[0] == 'Right Answer': temp[0] = dt[2]

                    if dt[0] == 'Wrong Answer': temp[1] = dt[2]

                    if dt[0] == 'No Answer': temp[2] = dt[2]



        edict[i] = temp

    # print(edict)



    for key, value in edict.items():

        right_ans_data.append(value[0])

        wrong_ans_data.append(value[1])

        no_ans_data.append(value[2])



    # print("wr", wrong_ans_data)

    # print("rt", right_ans_data)

    # print("no", no_ans_data)

    # print("event-", event_categories)



    wrong_answer = {

        'name': 'wrong_answer',

        'data': wrong_ans_data,

        'color': '#e53935'

    }

    right_answer = {

        'name': 'right_answer',

        'data': right_ans_data,

        'color': '#43a047'

    }

    no_answer = {

        'name': 'no_answer',

        'data': no_ans_data,

        'color': '#fb8c00'

    }



    bar_chart = {

        'chart': {'type': 'column',

                  },

        'title': {'text': 'Chatbot Log Summary(Bar Chart)',

                  'style': {

                      ' color': '#000',

                      'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

                  }

                  },

        'xAxis': {'categories': event_categories,

                  'title': {

                      'text': 'Date',

                      ' align': 'high'

                  }

                  },

        'yAxis': {



            'title': {

                'text': 'Count',

                ' align': 'high',

                'style': {

                    ' color': '#000',

                    'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

                }

            }

        },



        'series': [wrong_answer, right_answer, no_answer],

        'legend': {

            'itemStyle': {

                'font': '9pt Trebuchet MS, Verdana, sans-serif',

                'color': 'black'

            },

            'itemHoverStyle': {

                'color': 'red'

            },



        }

    }



    line_chart = {

        'chart': {'type': 'line'},

        'title': {'text': 'Chatbot Log Summary(Line Charts)',

                  'style': {

                      ' color': '#000',

                      'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif',

                  }

                  },

        'xAxis': {'categories': event_categories,

                  'title': {

                      'text': 'Date',

                      ' align': 'high'

                  }

                  },

        'yAxis': {

            'title': {

                'text': 'Count',

                ' align': 'high',

                'style': {

                    ' color': '#000',

                    'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

                }

            }

        },

        'series': [wrong_answer, right_answer, no_answer],

        'legend': {

            'itemStyle': {

                'font': '9pt Trebuchet MS, Verdana, sans-serif',

                'color': 'black'

            },

            'itemHoverStyle': {

                'color': 'red'

            },



        }



    }



    bar_dump = json.dumps(bar_chart)

    line_dump = json.dumps(line_chart)



    busy_count_list = []

    print("enaged--", en[0][0])
    
    for i in busy_count:

        if len(i[0]) > 5:

            busy_count_list.append(i)



    # for d in reset:

    #     print("---", d[1])

    # busy_count.remove(i)

    # print("busy_count_list", busy_count_list)
    print('reset', reset)



    context = {

        'reset_count': len(reset) if len(reset) == 0 else reset[0][1],

        # 'reset_count_time': reset_month[0][1],
        'live_count': len(live) if len(live) == 0 else live[0][1],
        'repeated_users': repeated_users,

        'busy_count': busy_count_list,

        'bar_chart': bar_dump,

        'line_chart': line_dump,

        'no_answer': pie_data[0][0], 'no_answer_count': pie_data[0][1],

        'rt_answer': pie_data[1][0], 'rt_answer_count': pie_data[1][1],

        'wr_answer': pie_data[2][0], 'wr_answer_count': pie_data[2][1],

        'total_users': en[0][0] + len(ne),

        'engaged_users': en[0][0],

        'new_users': len(ne),

        'users_list': users_list

    }

    return context





def monthly_charts():

    repeated_users = []

    reset, reset_month = [], []

    data, en, nu = get_monthly_data()

    pie_data = get_total_event_cnt()

    _, live_month = live_count()

    repeated_users = get_repeated_bot_monthly_users()

    busy_period_count_month = get_busy_period_count_monthly()

    # print("in busy_period_month - ", busy_period_count_month)

    event_categories = list()

    wrong_ans_data = list()

    right_ans_data = list()

    no_ans_data = list()

    reset, reset_month = reset_count()

    # print("len month data - ", len(data))

    for dt in data:

        if dt[1].__str__() not in event_categories:

            event_categories.append(dt[1].__str__())  # for answer desc



    edict = {}

    for i in event_categories:

        temp = [0, 0, 0]

        if i not in edict.keys():

            for dt in data:

                if i == dt[1].__str__():

                    if dt[0] == 'Right Answer': temp[0] = dt[2]

                    if dt[0] == 'Wrong Answer': temp[1] = dt[2]

                    if dt[0] == 'No Answer': temp[2] = dt[2]



        edict[i] = temp

    # print(edict)



    for key, value in edict.items():

        right_ans_data.append(value[0])

        wrong_ans_data.append(value[1])

        no_ans_data.append(value[2])



    # print("wrong_ans_data - ", wrong_ans_data)

    # print("right_ans_data - ", right_ans_data)

    # print("no_ans_data - ", no_ans_data)



    # print("from event categories -", event_categories)



    wrong_answer = {

        'name': 'wrong_answer',

        'data': wrong_ans_data,

        'color': '#e53935'

    }

    right_answer = {

        'name': 'right_answer',

        'data': right_ans_data,

        'color': '#43a047'

    }

    no_answer = {

        'name': 'no_answer',

        'data': no_ans_data,

        'color': '#fb8c00'

    }



    bar_chart = {

        'chart': {'type': 'column',

                  },

        'title': {'text': 'Chatbot Log Summary(Bar Chart)',

                  'style': {

                      ' color': '#000',

                      'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

                  }

                  },

        'xAxis': {'categories': event_categories,

                  'title': {

                      'text': 'Month',

                      ' align': 'high'

                  }

                  },

        'yAxis': {

            'title': {

                'text': 'Count',

                ' align': 'high',

                'style': {

                    ' color': '#000',

                    'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

                }

            }

        },



        'series': [wrong_answer, right_answer, no_answer],

        'legend': {

            'itemStyle': {

                'font': '9pt Trebuchet MS, Verdana, sans-serif',

                'color': 'black'

            },

            'itemHoverStyle': {

                'color': 'red'

            },



        }

    }



    line_chart = {

        'chart': {'type': 'line'},

        'title': {'text': 'Chatbot Log Summary(Line Charts)',

                  'style': {

                      ' color': '#000',

                      'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif',

                  }

                  },

        'xAxis': {'categories': event_categories,

                  'title': {

                      'text': 'Month',

                      ' align': 'high'

                  }

                  },

        'yAxis': {

            'title': {

                'text': 'Count',

                ' align': 'high',

                'style': {

                    ' color': '#000',

                    'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

                }

            }

        },

        'series': [wrong_answer, right_answer, no_answer],

        'legend': {

            'itemStyle': {

                'font': '9pt Trebuchet MS, Verdana, sans-serif',

                'color': 'black'

            },

            'itemHoverStyle': {

                'color': 'red'

            },



        }



    }



    bar_dump = json.dumps(bar_chart)

    line_dump = json.dumps(line_chart)

    temp_busy_count = []

    for i in busy_period_count_month:
        if i[0] != "": temp_busy_count.append(i)

    print('[info]', live_month)

    context = {

        'reset_month': reset_month[0][1],

        'repeated_users': repeated_users,

        'live_count': live_month[0][1],

        'busy_period_count_month': temp_busy_count,

        'total_users': len(en) + len(nu),

        'new_users': len(nu),

        'engaged_users': len(en),

        'bar_chart': bar_dump,

        'line_chart': line_dump,

        'no_answer': pie_data[0][0], 'no_answer_count': pie_data[0][1],

        'rt_answer': pie_data[1][0], 'rt_answer_count': pie_data[1][1],

        'wr_answer': pie_data[2][0], 'wr_answer_count': pie_data[2][1],

    }

    return context





def report(request, report_name):

    # print('==============================', report_name)

    if report_name == "Daily":

        context = daily_charts()

        return render(request, 'home/user_report.html', context)

    elif report_name == "Monthly":

        context = monthly_charts()

        return render(request, 'home/month_report.html', context)





def users(request):

    reports = Report.objects.values("assigned_to", "report_name")

    users_list = User.objects.filter(is_superuser=False)

    temp_list = []

    for i in reports:

        if i["report_name"] not in temp_list:

            temp_list.append(i["report_name"])



    print(temp_list)

    print(users_list)

    _user_reports = {}

    for user in users_list:

        _temp = []

        for report in reports:

            if user.id == report['assigned_to']:

                _temp.append(report['report_name'])

        if user.id not in _user_reports:

            _user_reports[user.id] = _temp



    print(_user_reports)



    if len(users_list) == 0:

        html = ""

        html += '<tr><td colspan=3>No Users Found</td></tr>'

        context = {

            'report_html': html,

        }

        return render(request, 'home/user_admin.html', context)

    else:

        html = ""

        for user in range(len(users_list)):

            html += '<tr><td>' + str(user + 1) + '</td><td>' + users_list[

                user].username + '</td><td><button class="dropbtn" id="' + str(user + 1) + '" onclick="show(' + str(

                user + 1) + ')" value="Reports Assigned">Reports Assigned</button></td>'

            for report in temp_list:

                html += '<tr class="show' + str(user + 1) + '" id="reports_hide"><td colspan="2">' + report + '</td>'

                inserted = False

                for key, value in _user_reports.items():

                    if users_list[user].id == key:

                        for i in value:

                            if i == report:

                                inserted = True

                                html += '<td><input type="checkbox" value="assigned" onclick=check(event,' + str(

                                    users_list[user].id) + ',"' + report + '") checked/></td>'

                if not inserted:

                    html += '<td><input type="checkbox" value="assigned" onclick=check(event,' + str(

                        users_list[user].id) + ',"' + report + '") /></td>'

                html += '</tr>'

            html += '</tr>'



        context = {

            'reports': temp_list,

            'user_list': users_list,

            'report_html': html,

        }



        return render(request, 'home/user_admin.html', context)





def update_report(request):

    print(request.POST)

    _report = Report.objects.get(report_name=request.POST["reportname"])

    print(_report)

    if request.POST['checked'] == 'true':

        _report.assigned_to.add(request.POST['userid'])

    else:

        _report.assigned_to.remove(request.POST['userid'])

    # return redirect('user')





@csrf_protect
@login_required(login_url="/login/")
def index(request):

    current_user = request.user

    # print(current_user.id)

    # print(current_user.username)

    users_list = User.objects.filter(is_superuser=False)



    if current_user.username == "admin":

        reports = Report.objects.values("assigned_to", "report_name")

        temp_list = []

        for i in reports:

            if i["report_name"] not in temp_list:

                temp_list.append(i["report_name"])



        return render(request, 'home/index_admin.html', {'userlist': users_list, 'reports': temp_list})



    else:

        reports = Report.objects.values("assigned_to", "report_name")

        temp_list = []

        for i in reports:

            if i["report_name"] not in temp_list and i['assigned_to'] == current_user.id:

                temp_list.append(i["report_name"])



        return render(request, 'home/user_adoreta.html', {'reports': temp_list})





@csrf_protect
@login_required(login_url="/login/")
def pages(request):

    context = {}

    # All resource paths end in .html.

    # Pick out the html file name from the url. And load that template.

    try:



        load_template = request.path.split('/')[-1]



        # print('load_template', load_template)



        if load_template == 'admin':

            return HttpResponseRedirect(reverse('admin:index'))

        context['segment'] = load_template



        html_template = loader.get_template('home/' + load_template)

        return HttpResponse(html_template.render(context, request))



    except template.TemplateDoesNotExist:



        html_template = loader.get_template('home/page-404.html')

        return HttpResponse(html_template.render(context, request))



    except:

        html_template = loader.get_template('home/page-500.html')

        return HttpResponse(html_template.render(context, request))





@csrf_protect
@login_required(login_url="/admin/")
def index_admin(request):

    context = {'segment': 'index_admin'}

    html_template = loader.get_template('home/index_admin.html')

    return HttpResponse(html_template.render(context, request))



# @csrf_protect

# @login_required(login_url="/login/")





# @csrf_protect

# @login_required(login_url="/login/")

# def supervisor_index(request):

#     current_user = request.user

#     users_list = User.objects.filter(is_superuser=False)

#     print("supervisor -> ", current_user.username)

#     data = get_monthly_data()

#     pie_data = get_total_event_cnt()

#     print("in supervisor")

#     pie_data_20 = get_2020_data()

#     pie_data_21 = get_2021_data()

#     event_categories = list()

#     wrong_ans_data = list()

#     right_ans_data = list()

#     no_ans_data = list()

#

#     wrong_ans_data21 = list()

#     right_ans_data21 = list()

#     no_ans_data21 = list()

#

#     for dt in data:

#         # print(dt)

#         if dt[0] == 'wrong answer':

#             wrong_ans_data.append(dt[2])

#         elif dt[0] == 'right answer':

#             right_ans_data.append(dt[2])

#         else:

#             no_ans_data.append(dt[2])

#

#         if dt[1].__str__() not in event_categories:

#             event_categories.append(dt[1].__str__())  # for answer desc

#

#     print(event_categories)

#     for dt in pie_data_20:

#         if dt[0] == 'wrong answer':

#             wrong_ans_data.append(dt[1])

#             # event_categories.append(dt[0].__str__())

#         elif dt[0] == 'right answer':

#             right_ans_data.append(dt[1])

#             # event_categories.append(dt[0].__str__())

#         else:

#             no_ans_data.append(dt[1])

#             # event_categories.append(dt[0].__str__())

#

#     for dt in pie_data_21:

#         if dt[0] == 'wrong answer':

#             wrong_ans_data21.append(dt[1])

#             # event_categories.append(dt[0].__str__())

#         elif dt[0] == 'right answer':

#             right_ans_data21.append(dt[1])

#             # event_categories.append(dt[0].__str__())

#         else:

#             no_ans_data21.append(dt[1])

#             # event_categories.append(dt[0].__str__())

#

#     wrong_answer = {

#         'name': 'wrong_answer',

#         'data': wrong_ans_data,

#         'color': '#e53935'

#     }

#     right_answer = {

#         'name': 'right_answer',

#         'data': right_ans_data,

#         'color': '#43a047'

#     }

#     no_answer = {

#         'name': 'no_answer',

#         'data': no_ans_data,

#         'color': '#fb8c00'

#     }

#

#     # print("event_categories-> ", event_categories)

#

#     bar_chart = {

#         'chart': {'type': 'column',

#                   },

#         'title': {'text': 'Chatbot Log Summary(Bar Chart)',

#                   'style': {

#                       ' color': '#000',

#                       'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

#                   }

#                   },

#         'xAxis': {'categories': event_categories,

#                   'title': {

#                       'text': 'Month',

#                       ' align': 'high'

#                   }

#                   },

#         'yAxis': {

#             'title': {

#                 'text': 'Count (thousands)',

#                 ' align': 'high',

#                 'style': {

#                     ' color': '#000',

#                     'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

#                 }

#             }

#         },

#

#         'series': [wrong_answer, right_answer, no_answer],

#         'legend': {

#             'itemStyle': {

#                 'font': '9pt Trebuchet MS, Verdana, sans-serif',

#                 'color': 'black'

#             },

#             'itemHoverStyle': {

#                 'color': 'red'

#             },

#

#         }

#     }

#

#     line_chart = {

#         'chart': {'type': 'line'},

#         'title': {'text': 'Chatbot Log Summary(Line Charts)',

#                   'style': {

#                       ' color': '#000',

#                       'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif',

#                   }

#                   },

#         'xAxis': {'categories': event_categories,

#                   'title': {

#                       'text': 'Date',

#                       ' align': 'high'

#                   }

#                   },

#         'yAxis': {

#             'title': {

#                 'text': 'Count (thousands)',

#                 ' align': 'high',

#                 'style': {

#                     ' color': '#000',

#                     'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

#                 }

#             }

#         },

#         'series': [wrong_answer, right_answer, no_answer],

#         'legend': {

#             'itemStyle': {

#                 'font': '9pt Trebuchet MS, Verdana, sans-serif',

#                 'color': 'black'

#             },

#             'itemHoverStyle': {

#                 'color': 'red'

#             },

#

#         }

#

#     }

#

#     wrong_answer_pie0 = {

#         'name': "wrong answer",

#         'y': wrong_ans_data[0],

#     }

#     right_answer_pie0 = {

#         'name': "right answer",

#         'y': right_ans_data[0],

#     }

#     no_answer_pie0 = {

#         'name': "no answer",

#         'y': no_ans_data[0],

#     }

#     pie_chart0 = {

#         'chart': {'type': 'pie',

#                   },

#         'plotOptions': {

#             'pie': {

#                 'dataLabels': {

#                     'enabled': 'true',

#                     'format': '<b>{point.name}</b>:<br>{point.percentage:.1f} %<br>value: {point.y}',

#                 }, 'showInLegend': 'true'

#             }

#         },

#         'title': {'text': 'Year - 2020',

#                   'style': {

#                       ' color': '#000',

#                       'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

#                   }

#                   },

#         'tooltip': {

#             'pointFormat': '{series.name}: <br>{point.percentage:.1f} %<br>value: {point.y}'

#         },

#

#         'series': [{

#             'data': [wrong_answer_pie0, right_answer_pie0, no_answer_pie0]

#         }],

#

#     }

#

#     # -----------------#

#     wrong_answer_pie1 = {

#         'name': "wrong answer",

#         'y': wrong_ans_data21[0],

#     }

#     right_answer_pie1 = {

#         'name': "right answer",

#         'y': right_ans_data21[0],

#     }

#     no_answer_pie1 = {

#         'name': "no answer",

#         'y': no_ans_data21[0],

#     }

#     pie_chart1 = {

#         'chart': {'type': 'pie',

#                   },

#         'plotOptions': {

#             'pie': {

#                 'dataLabels': {

#                     'enabled': 'true',

#                     'format': '<b>{point.name}</b>:<br>{point.percentage:.1f} %<br>value: {point.y}',

#                 }, 'showInLegend': 'true'

#             }

#         },

#         'title': {'text': 'Year - 2021',

#                   'style': {

#                       ' color': '#000',

#                       'font': 'bold 16px "Trebuchet MS", Verdana, sans-serif'

#                   }

#                   },

#         'tooltip': {

#             'pointFormat': '{series.name}: <br>{point.percentage:.1f} %<br>value: {point.y}'

#         },

#

#         'series': [{

#             'data': [wrong_answer_pie1, right_answer_pie1, no_answer_pie1]

#         }],

#

#     }

#

#

#     bar_dump = json.dumps(bar_chart)

#     line_dump = json.dumps(line_chart)

#     pie_dump0 = json.dumps(pie_chart0)

#     pie_dump1 = json.dumps(pie_chart1)

#     context = {

#         'bar_chart': bar_dump, 'line_chart': line_dump, 'pie_chart0': pie_dump0,

#         'pie_chart1': pie_dump1,

#         # 'pie_chart2': pie_dump2,

#         'no_answer': pie_data[0][0], 'no_answer_count': pie_data[0][1],

#         'rt_answer': pie_data[1][0], 'rt_answer_count': pie_data[1][1],

#         'wr_answer': pie_data[2][0], 'wr_answer_count': pie_data[2][1],

#         'users_list': users_list

#     }

#     return render(request, 'home/index_supervisor.html', context)


