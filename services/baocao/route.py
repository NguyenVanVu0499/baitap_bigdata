
from datetime import datetime
import json
import pandas as pd
from fastapi import APIRouter, Depends
from database.mongo import database
import os
import xlsxwriter
import string

router = APIRouter()

do_xe = database.get_collection("do_xe")
try:
    do_xe.create_index('ten_bien_so')
    do_xe.create_index('thoi_gian_vao')
    do_xe.create_index('thoi_gian_ra')
    do_xe.create_index('url_img')
    do_xe.create_index('trang_thai')
except Exception as error:
    print(error)

@router.get("/baocaothang", summary="Get all parking info")
async def baocaothang():
    query = {}
    info = []

    for n in do_xe.find(query):
        # n['_id'] = str(n['_id'])
        del n['_id']
        del n['url_img']
        del n['trang_thai']
        info.append(n)
    dates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31 ]
    total = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(len(info)):
        count = 0
        for j in info[i]['thoi_gian_vao']:
            for k in range(len(total)):
                # print(k, j.split('/')[0])
                if k == int(j.split('/')[0]):
                    total[k-1] += 1
    
    print(total)


    workbook = xlsxwriter.Workbook('chart.xlsx')
    worksheet = workbook.add_worksheet()

    # Create a new Chart object.
    chart = workbook.add_chart({'type': 'column'})

    # Write some data to add to plot on the chart.

    # worksheet.write_column('A1', dates)
    worksheet.write_column('B1', total)

    # Configure the chart. In simplest case we add one or more data series.
    # chart.add_series({'values': '=Sheet1!$A$1:$A$31'})
    chart.add_series({'values': '=Sheet1!$B$1:$B$31'})
    chart.set_size({'width': 820, 'height': 576})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('C7', chart)

    workbook.close()

    return info


 



