from dash import html, dcc
from dash.dependencies import Input, Output, State
import rich
from .. import ctrl_class
from ... data_cache import TriggerRecordData

def return_obj(dash_app, engine, storage):
    ctrl_id = "16_channel_number_ctrl"
    
    ctrl_div =html.Div([
        html.Div([
        html.Label("Select a Channel Number : ",style={"fontSize":"12px"}), html.Div([dcc.Dropdown(placeholder="Channel",
        id="channel_number_ctrl",multi=True)],style={"marginBottom":"1em","marginTop":"1em"},)])],id=ctrl_id)
    
    ctrl = ctrl_class.ctrl("channel_num", ctrl_id, ctrl_div, engine)
    ctrl.add_ctrl("08_adc_map_selection_ctrl")
    ctrl.add_ctrl("06_file_select_ctrl")
    ctrl.add_ctrl("07_trigger_record_select_ctrl")
    
    init_callbacks(dash_app, engine, storage )
    return(ctrl)

def init_callbacks(dash_app, engine, storage):
    @dash_app.callback(
        Output('channel_number_ctrl', 'options'),
        Input('adc_map_selection_ctrl', 'value'),Input("trigger_record_select_ctrl", 'value'),Input('file_select_ctrl', 'value')
        )
    def update_select(plane, trigger_record, raw_data_file):
        if not plane:
            return [""]

        if not trigger_record or not raw_data_file:
            return [""]
            
        try: 
            data = storage.get_trigger_record_data(trigger_record, raw_data_file)
        except RuntimeError:
            return [""]

        try: 
            channel_num=[]
            if "Z" in plane:
                channel_num.extend([{'label':str(n), 'value':(n)} for n in (data.df_Z.columns)])
            if "V" in plane:
                channel_num.extend( [{'label':str(n), 'value':(n)} for n in (data.df_V.columns)])
            if "U" in plane:
                channel_num.extend([{'label':str(n), 'value':(n)} for n in (data.df_U.columns)])
            return(channel_num)
        except RuntimeError :return([""])
        except TypeError: return([""])
