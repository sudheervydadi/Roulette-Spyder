from flask import Flask,render_template,request
import pandas as pd
import numpy as np
from datetime import datetime
import os


session_spins=pd.DataFrame(columns=['spin_landing','time','session_spin_count'])
session_spin_count=0

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():

    buttons=[' 1 ',' 2 ',' 3 ',' 4 ',' 5 ',' 6 ',' 7 ',' 8 ',' 9 ','10',
             '11','12','13','14','15','16','17','18','19','20',
             '21','22','23','24','25','26','27','28','29','30',
             '31','32','33','34','35','36',' 0 ']

    save_session=False
    undo_wrong=False

    if request.method=='GET':
        return render_template("roulette.html")

    if request.method=='POST':
        if request.form['button']=='Save Session':
            global session_spins
            save_session=True
            root_directory="C:/Users/sudhe/Desktop/GitHub Repository/Roulette-Spyder/Session Saves/"
            os.chdir(root_directory)
            session_spins.to_csv('session'+str(len(os.listdir(root_directory))+1)+'.csv')
            return render_template("roulette.html",save_session=save_session)

        if request.form['button']=='Undo':
            undo_wrong=True
            deleted_spin=session_spins.iloc[-1].spin_landing
            session_spins=session_spins[:-1]
            current_last_spin=session_spins.iloc[-1].spin_landing
            return render_template("roulette.html",undo_wrong=undo_wrong,current_last_spin=current_last_spin,deleted_spin=deleted_spin)

        if request.form['button'] in buttons:
            previous_buttonpress=request.form['button']
            spin_value_saver(previous_buttonpress)

            if len(session_spins)>=10:
                display_list=bid_helper()

                return render_template("roulette.html",previous_buttonpress=previous_buttonpress,display_list=display_list)

            return render_template("roulette.html",previous_buttonpress=previous_buttonpress)


    return render_template("roulette.html")


def spin_value_saver(previous_buttonpress):
    global session_spins
    global session_spin_count
    session_spin_count=session_spin_count+1
    session_spins=session_spins.append({'spin_landing':previous_buttonpress,
                                               'time':datetime.now(),
                                               'session_spin_count':session_spin_count},ignore_index=True)

    #print(session_spins.iloc[-1])

def bid_helper():
    #Here we have to do analysis and send back results to display
    return list([10,2,5,0,4,7,5])


if __name__=="__main__":
    app.run(debug=True)
