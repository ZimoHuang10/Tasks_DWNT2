from IPython.display import display, Image, clear_output, HTML
import time
import random
import os 
import pandas as pd
import numpy as np
import ipywidgets as widgets
from jupyter_ui_poll import ui_events

# load stimuli
s_stimuli        = ['small10vs9.png', 'small12vs9.png','small14vs12.png',
                  'small16vs12.png','small18vs16.png','small20vs15.png',
                    'small20vs18.png','small21vs18.png','small9vs10.png',
                    'small9vs12.png','small12vs14.png','small12vs16.png',
                    'small16vs18.png','small15vs20.png','small18vs20.png','small18vs21.png']
n_stimuli        = ['normal10vs9.png', 'normal12vs9.png','normal14vs12.png',
                  'normal16vs12.png','normal18vs16.png','normal20vs15.png',
                    'normal20vs18.png','normal21vs18.png','normal9vs10.png',
                    'normal9vs12.png','normal12vs14.png','normal12vs16.png',
                    'normal16vs18.png','normal15vs20.png','normal18vs20.png','normal18vs21.png']

stim_ans        = ['l','l','l','l','l','l','l','l','l','r','r','r','r','r','r','r','r']
stim_ans_button = ["Left" if ans == 'l' else "Right" if ans == 'r' else ans for ans in stim_ans]
stim_ratio      = [10/9, 12/9, 14/12, 16/12, 18/16, 20/15, 20/18, 21/18, 9/10, 9/12, 12/14, 12/16, 16/18, 15/20, 18/20, 18/21]
stim_ratio      = [round(ratio, 2) for ratio in stim_ratio]


n_stimuli_ratio_dict = dict(zip(n_stimuli, stim_ratio))
s_stimuli_ratio_dict = dict(zip(s_stimuli, stim_ratio))
n_stimuli_dict         = dict(zip(n_stimuli, stim_ans_button))
s_stimuli_dict         = dict(zip(s_stimuli, stim_ans_button))

# mix the plots
stimuliDict = n_stimuli_dict
stimuliDict.update(s_stimuli_dict)

stimuli_ratio_dict = n_stimuli_ratio_dict
stimuli_ratio_dict.update(s_stimuli_ratio_dict)

#


# for button press

event_info = {
    'type': '',
    'description': '',
    'time': -1
}

def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    with ui_events() as ui_poll: ui_poll(999) # add this line


    start_wait = time.time()

    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info

def wait_for_even_spatial(interval=0.001, max_rate=20, allow_interupt=True):
    start_wait = time.time()

    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate * interval) + 1

    with ui_events() as ui_poll:
        while True:
            ui_poll(n_proc)

            if allow_interupt and event_info['description'] != "":
                break

            time.sleep(interval)

    return event_info
# this function lets buttons 
# register events when clicked
def register_btn_event(btn):
    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

# send results 

import requests
from bs4 import BeautifulSoup
import json

def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form 
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok



def ans_test(id):

    gender = input('please enter your gender')
    
                                     
    answer = []    # participants's response 
    rt     = []    # reaction time per trial
    track  = []    # permutation tracking 

    n_trials = 32
    n_block  = 4
    stim = n_stimuli + s_stimuli

    rematrix = []
    # collect all response, 1 for correct, 0 for incorrect, -3 for missing 
    # length of matix will be number of trials 
    
    random.seed(1)    
    

    re     = []      # response, for checking the answering time window 
    score  = 0     # scoring initialization 
    list_ratio = []
    
    for b in range(n_block): # blockwise design or mix them together 
        random.shuffle(stim)
        for i in range (n_trials):
            
            bottom = widgets.Output(layout={"height":"60px"})
            # in range of trial numbers x blocks 
            # display fixation point
            fix = Image('fixation.png')
            display(fix)
            display(bottom)
            time.sleep(1.5)
            clear_output()
            
            # display ans stimuli
            dots=Image(stim[i])
            display(dots)
            display(bottom)
            time.sleep(0.75)
            clear_output()

            # tracking time window for answering 
            start_time = time.time()

           
            # back to fixation use a image to present the task instruction 
    
            bottom_area = widgets.Output(layout={"height":"60px"})
                    
            btn1 = widgets.Button(description="Left")
            btn2 = widgets.Button(description="Right")
                    
            btn1.on_click(register_btn_event)
            btn2.on_click(register_btn_event)

            btn1.layout.width = '500px'
            btn2.layout.width = '500px'
                    
            panel = widgets.HBox([btn1, btn2])
            bottom_area.append_display_data(panel)
        

            que = Image('question.png')
            display(que)
            display(bottom_area)

        
            re         = wait_for_event(timeout=3)
            # re = input("which side has more dots? left or right? (press l or r on keyboard)")
        
    
            end_time   = time.time()
            time_taken = end_time - start_time

            ratio = stimuli_ratio_dict[stim[i]]
            list_ratio.append(ratio)
            track.append(stim[i])

           # tracking time window for answering 
            # if out of 3s: labeled as mising answers
       
            if time_taken <= 3.0:
                answer.append(re['description'])
            else:
                answer.append('missing')

            # check valid answer for scoring and collect the type of response 
            if answer[len(answer)-1] == stimuliDict[stim[i]]:
                score +=1
                rematrix.append(1)
            elif answer[len(answer)-1] == 'missing':
                 rematrix.append(-3)
            else:
                score = score
                rematrix.append(0)
                
            # collect time used per trial 
            rt.append(time_taken)
            clear_output()
      
    _dict = {'button_response': answer, 'RT': rt, 'response_cat':rematrix, 'Stimuli_ratio': list_ratio, 'stim_used': track}
    
    result_df       = pd.DataFrame(_dict)
    result_df_tojsn = result_df.to_json()
    
    result_dict = {'Participant ID': id, 'score': score, 'gender': gender, 'result_json': result_df_tojsn}

    return result_dict

import glob
stimList = glob.glob('Slide*.png')
stimList.sort(key=lambda filename: int(filename[5:-4]))
correct_ans = ["C","B","A","B","C","C","B","D","D","B","A","D","C"]
stim_Ans = dict(zip(stimList,correct_ans))


def spatialReasoning(id):
                             
    answer = []    # participants's response 
    rt     = []    # reaction time per trial
    score  = 0
    rematrix = []

    for i in range(12):
        # tracking time window for answering 
        start_time = time.time()
    
        stim        = Image(stimList[i])
        display(stim)
    
        bottom_area = widgets.Output(layout={"height":"60px"})
                    
        btn1 = widgets.Button(description="A")
        btn2 = widgets.Button(description="B")
        btn3 = widgets.Button(description="C")
        btn4 = widgets.Button(description="D")
                
        btn1.on_click(register_btn_event)
        btn2.on_click(register_btn_event)
        btn3.on_click(register_btn_event)
        btn4.on_click(register_btn_event)

        btn1.layout.width = '250px'
        btn2.layout.width = '250px'
        btn3.layout.width = '250px'
        btn4.layout.width = '250px'
                
        panel = widgets.HBox([btn1, btn2,btn3,btn4])
        bottom_area.append_display_data(panel)
        display(bottom_area)

        re         = wait_for_even_spatial()
        end_time   = time.time()
        time_taken = end_time - start_time

        answer.append(re['description'])

        if answer[len(answer)-1] == stim_Ans[stimList[i]]:
            score +=1
            rematrix.append(1)
        else:
            score = score
            rematrix.append(0)
            
        # collect time used per trial 
        rt.append(time_taken)
        clear_output()
        
    _dict = {'Response': answer, 'RT': rt, 'response_cat':rematrix}
    
    result_df       = pd.DataFrame(_dict)
    result_df_tojsn = result_df.to_json()
    
    result_dict_spatial = {'Participant ID': id, 'score': score,
                   'result_json': result_df_tojsn}

    return result_dict_spatial

def data_consent():
        data_consent_info = """DATA CONSENT INFORMATION:
        
        Please read:
        
        we wish to record your response data
        
        to an anonymised public data repository.
        
        Your data will be used for educational teaching purposes
        
        practising data analysis and visualisation.
        
        Please type yes in the box below if you consent to the upload."""
        
        print(data_consent_info)
        
        result = input("> ")
        
        if result == "yes":
            
            print("Thanks for your participation.")
            
            print("Please contact philip.lewis@ucl.ac.uk")
            
            print("If you have any questions or concerns")
            
            print("regarding the stored results.")
        
        else:
        
        # end code execution by raising an exception
        
            raise(Exception("User did not consent to continue test."))


def id_instruction():
    id_instructions = """
    
    Enter your anonymised ID
    
    To generate an anonymous 4-letter unique user identifier please enter:
    
    - two letters based on the initials (first and last name) of a childhood friend
    
    - two letters based on the initials (first and last name) of a favourite actor / actress
    
    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
    
    then your unique identifer would be CBTC
    
    """
    
    print(id_instructions)
    
    user_id = input("> ")
    
    print("User entered id:", user_id)

    return user_id


def run_ts():

    data_consent()
    clear_output()
    
    id = id_instruction()
    clear_output()
    
    all_ = ans_test(id)
    send_to_google_form(data_dict = all_, 
                        form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSe-7g4EraDqz4HAUI0o1ed2inaMEJ3rWC-wzeWVN9RksPwqJA/viewform')
    display(Image('endAns.png'))
    time.sleep(5.0)
    clear_output()
    all_spatial = spatialReasoning(id)
    send_to_google_form(data_dict = all_spatial, 
                        form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeu5b4yiwPQuxH5b-c0OfEjs5-SulrM2P-PgmP0Y7Blr_YDCg/viewform?usp=sf_link')
    display(Image('endAll.png'))
    time.sleep(2.0)
    clear_output()
    
    return 



