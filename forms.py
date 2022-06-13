from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, SubmitField, DecimalField, RadioField, TextField, PasswordField
from wtforms import validators
from wtforms.fields.simple import PasswordField
from wtforms.i18n import messages_path
from wtforms.validators import DataRequired, Length, NumberRange, Email, InputRequired, EqualTo

class ScenarioForm(FlaskForm):
    choices_network = [('Wi-Fi 802.11ac', 'Wi-Fi 802.11ac'), ('Wi-Fi 802.11ax', 'Wi-Fi 802.11ax'), ('LoRaWAN', 'LoRaWAN'), ('6LoWPAN', '6LoWPAN'), ('Wi-Fi HaLow', 'Wi-Fi HaLow')] 
    choices_MCS = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),
                    ('9', '9'),('10', 'Ideal Wi-Fi manager')]
    #choices_bandwidth = [(20, '20'),(40, '40'),(80, '80'),(160, '160')]
    choices_spatial_streams = [('1', '1'), ('2', '2'),('4', '4')]
    choices_sf = [('0','LoRaWAN manager'), ('7','7'), ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12')]
    choices_prop_delay = [(0,'ConstantSpeedPropagationDelayModel'), (1,'RandomPropagationDelayModel')]
    choices_radio_environment = [(0,'Urban'), (1,'Suburban'), (2,'Rural'), (3,'Indoor')]

    network = SelectField('Type of network', choices=choices_network, default='Wi-Fi 802.11ac')
    traffic_dir = SelectField('Traffic direction', choices=[('upstream','Upstream'),('downstream', 'Downstream')], validators=[DataRequired()], default='upstream') 
    traffic_profile = SelectField('Traffic profile', choices=[('periodic','Periodic'),('cbr','CBR'),('vbr','VBR')], validators=[DataRequired()], default='periodic')
    packet_size_wifi = IntegerField('Packet size, bytes', validators=[DataRequired(), NumberRange(min=1,max=1500,message='Packet size must be between 1 and 1500 bytes.')],default=1024)
    packet_size_lorawan = IntegerField('Packet size, bytes', validators=[DataRequired(), NumberRange(min=1,max=230,message='Packet size must be between 1 and 230 bytes.')], default=23)
    packet_size_6lowpan = IntegerField('Packet size, bytes', validators=[DataRequired(), NumberRange(min=1,max=1000,message='Packet size must be between 1 and 1000 bytes.')], default=50)
    load_freq = IntegerField('Packet period, seconds', validators=[DataRequired(), NumberRange(min=0, message='Load frequency must not be negative.')], default=1)
    mean_load = IntegerField('Mean load, Mbps', validators=[DataRequired(), NumberRange(min=0, message='Mean load must not be negative.')], default=2)
    fps = IntegerField('FPS, Frames per Second', validators=[DataRequired(), NumberRange(min=0, message='FPS must not be negative.')], default=30)
    mean = IntegerField('Mean of packet size variable', validators=[DataRequired(), NumberRange(min=0, message='Mean must not be negative.')], default=1500)
    variance = IntegerField('Variance of packet size variable', validators=[DataRequired(), NumberRange(min=0, message='Variance must not be negative.')], default=100)
    num_devices = IntegerField('Number of end-devices', validators=[DataRequired(), NumberRange(min=1, message='Number of end-devices must not be negative.')]) 
    dist_devices_gateway = IntegerField('Distance end-devices-gateway, meter', validators=[DataRequired(), NumberRange(min=0, message='Distance between gateway and end-devices must not be negative.')])
    simulation_time = IntegerField('Simulation time, seconds', validators=[DataRequired(), NumberRange(min=0, message='Time must be > 5s')])
    hidden_devices = RadioField('Hidden devices?', choices = [('1', 'Yes'), ('0', 'No')], default='0')
    change = BooleanField('Change advanced parameters', default=0)
    prop_delay = SelectField('Propagation Delay Model', choices = choices_prop_delay, default=0, coerce=int)
    radio_environment = SelectField('Radio Environment', choices = choices_radio_environment, default=0, coerce=int)
    sf = SelectField('Spreading factor (SF)',choices= choices_sf, default='0')
    cyclic_redundacy_check = SelectField('Cyclic Redundacy Check', choices = [('1', 'Enabled'), ('0','Disabled')], default='1') 
    coding_rate = SelectField('Coding Rate', choices = [('1', '4:5'), ('2','4:6'), ('3','4:7'), ('4','4:8')], default='1') 
    confirmed_traffic = SelectField('Type of Traffic', choices = [('Confirmed', 'Confirmed'), ('Unconfirmed','Unconfirmed')], default='Unconfirmed')
    min_BE = IntegerField('Min BE',validators=[DataRequired(), NumberRange(min=0, message='Min BE must not be negative.')], default=3)
    max_BE = IntegerField('Max BE',validators=[DataRequired(), NumberRange(min=0, message='Max BE must not be negative.')], default=5)
    csma_backoffs = IntegerField('CSMA Backoffs',validators=[DataRequired(), NumberRange(min=0, message='Must not be negative.')], default=4)
    max_frame_retries = IntegerField('Max Frame Retries',validators=[DataRequired(), NumberRange(min=0, message='Must not be negative.')], default=5)
    beacon_interval = IntegerField('Beacon Interval, ms', validators=[DataRequired(), NumberRange(min=0, message='Must not be negative.')], default=51200)
    mcs = SelectField('MCS', choices=choices_MCS, default='10')
    bandwidth = SelectField('Bandwidth', choices=[])
    spatial_streams = SelectField('Spatial streams', choices=choices_spatial_streams, default='1')
    tx_current = DecimalField('Tx current draw, mA', validators=[DataRequired(), NumberRange(min=0, message='Tx current draw must not be negative.')], default=107)
    rx_current = DecimalField('Rx current draw, mA', validators=[DataRequired(), NumberRange(min=0, message='Rx current draw must not be negative.')], default=40)
    idle_current = DecimalField('Idle current draw, mA',validators=[DataRequired(), NumberRange(min=0, message='Idle current draw must not be negative.')], default=1)
    cca_busy_current = DecimalField('CCA_Busy current draw, mA',validators=[DataRequired(), NumberRange(min=0, message='CCA_Busy current draw must not be negative.')], default=1)
    sleep_current = DecimalField('Sleep current draw, mA',validators=[DataRequired(), NumberRange(min=0, message='Sleep current draw must not be negative.')], default=0.01)
    voltage = DecimalField('Voltage, volts',validators=[DataRequired(), NumberRange(min=0, message='Voltage must not be negative.')], default=12)
    battery_cap = IntegerField('Battery capacity, mAh',validators=[DataRequired(), NumberRange(min=0, message='Battery capacity must not be negative.')], default=5200)
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired(), Length(max=20)])
    email = TextField('Email', validators=[InputRequired(), Email(message="Invalid email!"), Length(max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Both password fields must be match!')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = TextField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [InputRequired()])
    submit = SubmitField('Submit')