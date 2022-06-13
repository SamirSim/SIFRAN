var diagram = document.getElementById("img_traffic");
var network = document.getElementById("network");
var direction = document.getElementById("traffic_direction");
var traffic_profile = document.getElementById("traffic_profile");
network.addEventListener("change", onChangeSelectNetwork);
direction.addEventListener("change", onChangeSelectDirection);
traffic_profile.addEventListener("change", onChangeSelectTrafficProfile);
traffic_profile.value = 'periodic';
var load_freq = document.getElementById("load_freq");
var lbl_load_freq = document.getElementById("lbl_load_freq");
var mean_load =document.getElementById("mean_load");
var lbl_mean_load = document.getElementById("lbl_mean_load");

//hiding load_freq and mean_load before choosing traffic profile
load_freq.style.display = "inherit";
lbl_load_freq.style.display = "inherit";
mean_load.style.display = "none";
lbl_mean_load.style.display = "none";

var lbl_sf = document.getElementById("lbl_sf");
var sf = document.getElementById("sf");

var num_devices = document.getElementById("num_devices");
var dist_devices_gateway = document.getElementById("dist_devices_gateway");
var simulation_time = document.getElementById("simulation_time");

var lbl_prop_delay = document.getElementById("lbl_prop_delay");
var prop_delay = document.getElementById("prop_delay");
var lbl_radio_environment = document.getElementById("lbl_radio_environment");
var radio_environment = document.getElementById("radio_environment");
var lbl_cyclic_redundacy_check = document.getElementById("lbl_cyclic_redundacy_check");
var cyclic_redundacy_check = document.getElementById("cyclic_redundacy_check");
var lbl_coding_rate  = document.getElementById("lbl_coding_rate");
var coding_rate  = document.getElementById("coding_rate");
var lbl_confirmed_traffic  = document.getElementById("lbl_confirmed_traffic");
var confirmed_traffic  = document.getElementById("confirmed_traffic");

var lbl_min_BE  = document.getElementById("lbl_min_BE");
var min_BE  = document.getElementById("min_BE");
var lbl_max_BE  = document.getElementById("lbl_max_BE");
var max_BE  = document.getElementById("max_BE");
var lbl_csma_backoffs  = document.getElementById("lbl_csma_backoffs");
var csma_backoffs  = document.getElementById("csma_backoffs");
var lbl_max_frame_retries  = document.getElementById("lbl_max_frame_retries");
var max_frame_retries  = document.getElementById("max_frame_retries");

var lbl_mcs = document.getElementById("lbl_mcs");
var mcs = document.getElementById("mcs");
var lbl_fps = document.getElementById("lbl_fps");
var fps = document.getElementById("fps");
var lbl_mean = document.getElementById("lbl_mean");
var mean = document.getElementById("mean");
var lbl_variance = document.getElementById("lbl_variance");
var variance = document.getElementById("variance");
var lbl_bandwidth = document.getElementById("lbl_bandwidth");
var bandwidth = document.getElementById("bandwidth");
var lbl_spatial_streams = document.getElementById("lbl_spatial_streams");
var spatial_streams = document.getElementById("spatial_streams");
var lbl_tx_current = document.getElementById("lbl_tx_current");
var tx_current = document.getElementById("tx_current");
var lbl_rx_current = document.getElementById("lbl_rx_current");
var rx_current = document.getElementById("rx_current");
var lbl_idle_current = document.getElementById("lbl_idle_current");
var idle_current = document.getElementById("idle_current");
var lbl_cca_busy_current = document.getElementById("lbl_cca_busy_current");
var cca_busy_current = document.getElementById("cca_busy_current");
var lbl_sleep_current = document.getElementById("lbl_sleep_current");
var sleep_current = document.getElementById("sleep_current");
var lbl_battery_cap = document.getElementById("lbl_battery_cap");
var battery_cap = document.getElementById("battery_cap");

//hiding all advanced parameters if checkboxChange is unchecked 

lbl_prop_delay.style.display = "none";
prop_delay.style.display = "none";
lbl_radio_environment.style.display = "none";
radio_environment.style.display = "none";
lbl_cyclic_redundacy_check.style.display = "none";
cyclic_redundacy_check.style.display = "none";
lbl_coding_rate.style.display = "none";
coding_rate.style.display = "none";
lbl_confirmed_traffic.style.display = "none";
confirmed_traffic.style.display = "none";

lbl_min_BE.style.display = "none";
min_BE.style.display = "none";
lbl_max_BE.style.display = "none";
max_BE.style.display = "none";
lbl_csma_backoffs.style.display = "none";
csma_backoffs.style.display = "none";
lbl_max_frame_retries.style.display = "none";
max_frame_retries.style.display = "none";

lbl_mcs.style.display = "none";
mcs.style.display = "none";
lbl_fps.style.display = "none";
fps.style.display = "none";
lbl_mean.style.display = "none";
mean.style.display = "none";
lbl_variance.style.display = "none";
variance.style.display = "none";
//hiding SF before choosing LoRaWAN
lbl_sf.style.display = "none";
sf.style.display = "none";     
lbl_bandwidth.style.display = "none";
bandwidth.style.display = "none";
lbl_spatial_streams.style.display = "none";
spatial_streams.style.display = "none";
lbl_tx_current.style.display = "none";
tx_current.style.display = "none";
lbl_rx_current.style.display = "none";
rx_current.style.display = "none";
lbl_idle_current.style.display = "none";
idle_current.style.display = "none";
lbl_cca_busy_current.style.display = "none";
cca_busy_current.style.display = "none";
lbl_sleep_current.style.display = "none";
sleep_current.style.display = "none";
lbl_voltage.style.display = "none";
voltage.style.display = "none";
lbl_battery_cap.style.display = "none";
battery_cap.style.display = "none";

//Hide spinner loading 
const spinner = document.getElementById("spinner");
spinner.style.display = "none";
const submit_btn = document.getElementById("submit_btn");
//Toggle spinner loading when click submit button
submit_btn.addEventListener("click", function() {
    var packet_size_wifi_indicator = document.getElementById("packet_size_wifi").value;
    var packet_size_lorawan_indicator = document.getElementById("packet_size_lorawan").value;
    var packet_size_6lowpan_indicator = document.getElementById("packet_size_6lowpan").value;
    var num_devices_indicator = document.getElementById("num_devices").value;
    var dist_devices_gateway_indicator = document.getElementById("dist_devices_gateway").value;
    var simulation_time_indicator = document.getElementById("simulation_time").value;
    var load_freq_indicator = document.getElementById("load_freq").value;
    var mean_load_indicator = document.getElementById("mean_load").value;
    var fps_indicator = document.getElementById("fps").value;
    var mean_indicator = document.getElementById("mean").value;
    var variance_indicator = document.getElementById("variance").value;
    var tx_current_indicator = document.getElementById("tx_current").value;
    var rx_current_indicator = document.getElementById("rx_current").value;
    var idle_current_indicator = document.getElementById("idle_current").value;
    var cca_busy_current_indicator = document.getElementById("cca_busy_current").value;
    var battery_cap_indicator = document.getElementById("battery_cap").value;
    var voltage_indicator = document.getElementById("voltage").value;
    
   if (!simulation_time_indicator == ' ' && !packet_size_wifi_indicator == ' ' &&
       !packet_size_lorawan_indicator == ' ' && !packet_size_6lowpan_indicator == ' ' &&
    !num_devices_indicator == ' ' &&
       !dist_devices_gateway_indicator == ' ' && !load_freq_indicator == ' ' &&
       !mean_load_indicator == ' ' && !fps_indicator == ' ' && 
       !mean_indicator == ' ' && !variance_indicator == ' ' &&
       !tx_current_indicator == ' ' && !rx_current_indicator == ' ' &&
       !idle_current_indicator == ' ' && !cca_busy_current_indicator == ' ' &&
       !battery_cap_indicator == ' ' && !voltage_indicator == ' ') {
        spinner.style.display = "inherit";
    }
    //setTimeout(stopSpinner,99999999);
});

function stopSpinner(){
    spinner.style.display = "none";
}

var checkboxChange = document.getElementById("change");
checkboxChange.addEventListener("change", onChangeCheckbox);

function onChangeCheckbox(){
    onCheck();
}

function onCheck(){
    if (checkboxChange.checked) {
        lbl_prop_delay.style.display = "inherit";
        prop_delay.style.display = "inherit";
        lbl_radio_environment.style.display = "inherit";
        radio_environment.style.display = "inherit";
        lbl_bandwidth.style.display = "inherit";
        bandwidth.style.display = "inherit";
        lbl_tx_current.style.display = "inherit";
        tx_current.style.display = "inherit";
        lbl_rx_current.style.display = "inherit";
        rx_current.style.display = "inherit";
        lbl_idle_current.style.display = "inherit";
        idle_current.style.display = "inherit";
        lbl_voltage.style.display = "inherit";
        voltage.style.display = "inherit";
        lbl_battery_cap.style.display = "inherit";
        battery_cap.style.display = "inherit";

        if (network.value =='Wi-Fi 802.11ac' || network.value == 'Wi-Fi 802.11ax' || network.value == 'Wi-Fi HaLow') {
            lbl_mcs.style.display = "inherit";
            mcs.style.display = "inherit";
            lbl_spatial_streams.style.display = "inherit";
            spatial_streams.style.display = "inherit";
            lbl_cca_busy_current.style.display = "inherit";
            cca_busy_current.style.display = "inherit";
        }
        else if (network.value == "LoRaWAN") {
            //advanced parameters of LoRaWAN shown
            lbl_cyclic_redundacy_check.style.display = "inherit";
            cyclic_redundacy_check.style.display = "inherit";
            lbl_coding_rate.style.display = "inherit";
            coding_rate.style.display = "inherit";
            lbl_confirmed_traffic.style.display = "inherit";
            confirmed_traffic.style.display = "inherit";
            lbl_sf.style.display = "inherit";
            sf.style.display = "inherit";
            lbl_sleep_current.style.display = "inherit";
            sleep_current.style.display = "inherit";
        } 
        else if (network.value == "6LoWPAN") {
            lbl_min_BE.style.display = "inherit";
            min_BE.style.display = "inherit";
            lbl_max_BE.style.display = "inherit";
            max_BE.style.display = "inherit";
            lbl_csma_backoffs.style.display = "inherit";
            csma_backoffs.style.display = "inherit";
            lbl_max_frame_retries.style.display = "inherit";
            max_frame_retries.style.display = "inherit";
        } 
        
    }
    else {
        lbl_prop_delay.style.display = "none";
        prop_delay.style.display = "none";
        lbl_radio_environment.style.display = "none";
        radio_environment.style.display = "none";
        lbl_cyclic_redundacy_check.style.display = "none";
        cyclic_redundacy_check.style.display = "none";
        lbl_coding_rate.style.display = "none";
        coding_rate.style.display = "none";
        lbl_confirmed_traffic.style.display = "none";
        confirmed_traffic.style.display = "none";

        lbl_min_BE.style.display = "none";
        min_BE.style.display = "none";
        lbl_max_BE.style.display = "none";
        max_BE.style.display = "none";
        lbl_csma_backoffs.style.display = "none";
        csma_backoffs.style.display = "none";
        lbl_max_frame_retries.style.display = "none";
        max_frame_retries.style.display = "none";        
       
        lbl_mcs.style.display = "none";
        mcs.style.display = "none";
        //lbl_fps.style.display = "none";
        fps.style.display = "none";
        mean.style.display = "none";
        variance.style.display = "none";
        lbl_sf.style.display = "none";
        sf.style.display = "none";     
        lbl_bandwidth.style.display = "none";
        bandwidth.style.display = "none";
        lbl_spatial_streams.style.display = "none";
        spatial_streams.style.display = "none";
        lbl_tx_current.style.display = "none";
        tx_current.style.display = "none";
        lbl_rx_current.style.display = "none";
        rx_current.style.display = "none";
        lbl_idle_current.style.display = "none";
        idle_current.style.display = "none";
        lbl_cca_busy_current.style.display = "none";
        cca_busy_current.style.display = "none";
        lbl_sleep_current.style.display = "none";
        sleep_current.style.display = "none";
        lbl_voltage.style.display = "none";
        voltage.style.display = "none";
        lbl_battery_cap.style.display = "none";
        battery_cap.style.display = "none";
    }
}

    

//Preset radiobuttons for all parameters
    var packet_size_wifi = document.getElementById("packet_size_wifi");
    var lbl_packet_size_wifi = document.getElementById("lbl_packet_size_wifi");
    var packet_size_lorawan = document.getElementById("packet_size_lorawan");
    var lbl_packet_size_lorawan = document.getElementById("lbl_packet_size_lorawan");
    var packet_size_6lowpan = document.getElementById("packet_size_6lowpan");
    var lbl_packet_size_6lowpan = document.getElementById("lbl_packet_size_6lowpan");
    var wifi_error = document.getElementById("wifi_error");
    var lorawan_error = document.getElementById("lorawan_error");
    var sixlowpan_error = document.getElementById("sixlowpan_error");
    var dist_devices_gateway_error = document.getElementById("dist_devices_gateway_error");
    var simulation_time_error = document.getElementById("simulation_time_error");
    var num_devices_error = document.getElementById("num_devices_error");
    var fps_error = document.getElementById("fps_error");
    var mean_error = document.getElementById("mean_error");
    var variance_error = document.getElementById("variance_error");

  
//hide packet sizes fields
console.log("wifi-error :"+wifi_error.innerText.length);
console.log("LoRaWAN error :"+lorawan_error.innerText.length);
console.log("6LoWPAN error :"+sixlowpan_error.innerText.length);
if(wifi_error.innerText.length!=0)
{
    packetSizeShow("Wi-Fi");
}
else if(lorawan_error.innerText.length!=0)
{
    packetSizeShow("LoRaWAN");
}
else if(sixlowpan_error.innerText.length!=0)
{
    packetSizeShow("6LoWPAN");
}   
else
{
    packetSizeShow("");
} 


 //function for show packet size field
 function packetSizeShow(networkType){
    if (networkType=="Wi-Fi")
    {
        lbl_packet_size_wifi.style.display = "inherit";
        packet_size_wifi.style.display = "inherit";
        wifi_error.style.display = "inherit";
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_lorawan.style.display = "none";
        lorawan_error.style.display = "none";
        lbl_packet_size_6lowpan.style.display = "none";
        packet_size_6lowpan.style.display = "none";
        sixlowpan_error.style.display = "none";

    }
    else if (networkType=="Wi-Fi HaLow")
    {
        lbl_packet_size_wifi.style.display = "inherit";
        packet_size_wifi.style.display = "inherit";
        wifi_error.style.display = "inherit";
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_lorawan.style.display = "none";
        lorawan_error.style.display = "none";
        lbl_packet_size_6lowpan.style.display = "none";
        packet_size_6lowpan.style.display = "none";
        sixlowpan_error.style.display = "none";

    }
    else if (networkType=="LoRaWAN")
    {
        lbl_packet_size_lorawan.style.display = "inherit";
        packet_size_lorawan.style.display = "inherit";
        lorawan_error.style.display = "inherit";
        lbl_packet_size_wifi.style.display = "none";
        packet_size_wifi.style.display = "none";
        wifi_error.style.display = "none";
        lbl_packet_size_6lowpan.style.display = "none";
        packet_size_6lowpan.style.display = "none";
        sixlowpan_error.style.display = "none";
    }
    else if (networkType=="6LoWPAN")
    {
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_lorawan.style.display = "none";
        lorawan_error.style.display = "none";
        lbl_packet_size_wifi.style.display = "none";
        packet_size_wifi.style.display = "none";
        wifi_error.style.display = "none";
        lbl_packet_size_6lowpan.style.display = "inherit";
        packet_size_6lowpan.style.display = "inherit";
        sixlowpan_error.style.display = "inherit";
    }
    else {
        //hide packet sizes fields
        lbl_packet_size_wifi.style.display = "none";
        packet_size_wifi.style.display = "none";
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_lorawan.style.display = "none";
        lbl_packet_size_6lowpan.style.display = "none";
        packet_size_6lowpan.style.display = "none";
        wifi_error.style.display = "none";
        lorawan_error.style.display = "none";
        sixlowpan_error.style.display = "none";
    }
 }   

 function clearErrors(){
     wifi_error.innerText = "";
     lorawan_error.innerText = "";
     sixlowpan_error.innerText = "";
     num_devices_error.innerText = "";
     fps_error.innerText = "";
     mean_error.innerText = "";
     variance_error.innerText = "";
     dist_devices_gateway_error.innerText = "";
     simulation_time_error.innerText = "";
 }

 function selectBandwidth(selectNetwork){
     switch(selectNetwork){
          //set a bandwidth label depending on a network
        case 'LoRaWAN':
                lbl_bandwidth.textContent = "Bandwidth, KHz"
                optionBandwidth = '<option selected value="125">125</option>'+
                                '<option value="250">250</option>'+
                                '<option value="500">500</option>';
                break;        
        case '6LoWPAN': 
                lbl_bandwidth.textContent = "Bandwidth, MHz"
                optionBandwidth = '<option selected value="5">5</option>';
                break;
        case 'Wi-Fi HaLow': 
                lbl_bandwidth.textContent = "Bandwidth, MHz"
                optionBandwidth = '<option selected value ="2">2</option>';
                break;
        default :  
                 lbl_bandwidth.textContent = "Bandwidth, MHz"
                 optionBandwidth = '<option value="20">20</option>'+
                                   '<option selected value="80">80</option>'+
                                   '<option value="160">160</option>';
     }
     bandwidth.innerHTML = optionBandwidth;
 }
    
    //Uncheck checkboxChange after reload/submit
    checkboxChange.checked = false;
    //set Bandwith according to selected network
    selectBandwidth(network.value);
    var preset = document.querySelectorAll('input[name="radioPreset"]');
    var select_preset = false;

    for(let i=0; i<preset.length; i++)
    {
        console.log("Preset"+preset[i].value);
        preset[i].addEventListener("change", function(){
            if(this.checked)
            {
                //uncheck checkboxChange
                checkboxChange.checked = false;
                onCheck();
                //clear packet size error fields
                clearErrors();  
                select_preset = this.value;
                console.log("Selected preset value :"+select_preset);
                //Add full choices of traffic direction and traffic profile before preset
                var optionDirection ='<option value="upstream">Upstream</option>'+
                                    '<option value="downstream">Downstream</option>';
                var optionProfile = '<option value="periodic">Periodic</option>'+
                                    '<option value="cbr">CBR</option>'+
                                    '<option value="vbr">VBR</option>';
                direction.innerHTML = optionDirection;
                traffic_profile.innerHTML = optionProfile;
                
                var optionBandwidth = "";
                if (select_preset != "4")
                {                   
                   //set a default value to battery capacity depending on a network, here is wifi
                    battery_cap.value = "2400";
                    voltage.value = "3";
                    packetSizeShow("Wi-Fi");        
                }
                else
                {
                    //set a default value to battery capacity depending on a network, here is LoRaWAN
                    battery_cap.value = "2400";    
                    voltage.value = "3";   
                    packetSizeShow("LoRaWAN");    
                                    
                }

                switch(select_preset) {
                    case '1'://Telemetry 
                        network.selectedIndex = "0";            //set to Wi-Fi 5
                        console.log("Selected network =", network.value);
                        direction.selectedIndex = "0";          //set to Upstream
                        traffic_profile.selectedIndex = "0";    //set to Periodic
                        packet_size_wifi.value = "1024";             //set to 1024 bytes
                        load_freq.value = "1";                  //set to 1 packet/sec
                        num_devices.value = "1";                //set to 20 devices
                        dist_devices_gateway.value = "20";       //set distance to 10 meter
                        simulation_time.value = "10";
                        radio_environment.value = 0;
                        tx_current.value = "107";
                        rx_current.value = "40";
                        idle_current.value = "1";
                        //The rest advanced parameter are set to default; listed in the documentation
                        //Set a picture to upstream direction
                        //diagram.setAttribute('src', '../static/img/diagram_traffic_upstream.png');
                        break;
                    case '2'://Video-surveillance 
                        network.selectedIndex = "0";             //set to Wi-Fi 5  
                        console.log("Selected network =", network.value);
                        console.log("Selected index = ", network.selectedIndex);
                        direction.selectedIndex = "0";          //set to Upstream
                        traffic_profile.selectedIndex = "1";    //set to Stochastic
                        packet_size_wifi.value = "1500";             //set to 1024 bytes
                        mean_load.value = "2";                  //set to 2 Mbps
                        num_devices.value = "5";                //set to 5 devices
                        //fps.value = "30";                //FPS=30
                        dist_devices_gateway.value = "10";       //set distance to 1 meter
                        simulation_time.value = "5";
                        radio_environment.value = 1;
                        tx_current.value = "107";
                        rx_current.value = "40";
                        idle_current.value = "1";
                        //The rest advanced parameter are set to default; listed in the documentation
                        //diagra.SetAttribute('src', '../static/img/diagram_traffic_upstream.png');
                        break;
                    case '3'://Webcast
                        network.selectedIndex = "0";             //set to Wi-Fi 5 
                        console.log("Selected network =", network.value);
                        direction.selectedIndex = "1";          //set to Downstream
                        traffic_profile.selectedIndex = "1";    //set to Stochastic
                        packet_size_wifi.value = "1500";            //set to 1024 bytes
                        mean_load.value = "2";                  //set to 2 Mbps
                        num_devices.value = "5";               //set to 20 devices
                        dist_devices_gateway.value = "10";       //set distance to 1 meter
                        simulation_time.value = "5";
                        radio_environment.value = 1;
                        tx_current.value = "107";
                        rx_current.value = "40";
                        idle_current.value = "1";
                        //The rest advanced parameter are set to default; listed in the documentation
                        //Set the picture to downstream direction
                        //diagra.SetAttribute('src', '../static/img/diagram_traffic_downstream.png');
                        break;
                    case '4'://smart metering
                        network.selectedIndex = "2";             //set to LoRaWAN
                        console.log("Selected network =", network.value);
                        direction.selectedIndex = "0";          //set to Upstream
                        traffic_profile.selectedIndex = "0";    //set to Periodic
                        packet_size_lorawan.value = "23";               //set to 23 bytes
                        load_freq.value = "360";           //set to 3600 packet/sec or 1 packet/hr
                        num_devices.value = "10" ;           //set to 10 devices
                        dist_devices_gateway.value = "1000";    //set distance to 100 m
                        simulation_time.value = "3600";
                        tx_current.value = "77";
                        rx_current.value = "28";
                        sf.selectedIndex = "0";                 //set SF to 0 (default)
                        optionDirection = '<option selected value="upstream">Upstream</option>';
                        optionProfile = '<option selected value="periodic">Periodic</option>';  
                        direction.innerHTML = optionDirection;
                        traffic_profile.innerHTML = optionProfile;
                        radio_environment.value = 2;
                        //The rest advanced parameter are set to default; listed in the documentation
                        //diagra.SetAttribute('src', '../static/img/diagram_traffic_upstream.png');
                        break;
                }   
                //Set meanload or load freq according to traffic direction
                onChangeTrafficProfile();
                //set choices to bandwidth depending on a network
                selectBandwidth(network.value);
            }
        });   
        
    }

function clearPresetRdb(){
    preset.forEach(element => {
        element.checked = false;
    });
}
//if a user selects or inputs parameters by himself or herself, uncheck preset radiobuttons
const selectedItems = document.querySelectorAll(".form-select, .form-control");
console.log("Number of selected items : "+selectedItems.length);
selectedItems.forEach(selectedItem => {
    selectedItem.addEventListener("change", function(){
        //uncheck preset radiobuttons
        clearPresetRdb();
        
    });
});

function onChangeSelectNetwork(){
   var select_network = network.value;
   console.log("selected network:"+select_network);
   var optionDirection="";
   var optionProfile="";
   var optionBandwidth = "";
   //uncheck checkboxChange
   checkboxChange.checked = false;
    onCheck();
    //clear packet size error fields
    clearErrors(); 
    //set seclect Bandwidth
    selectBandwidth(select_network);

    if (select_network == 'Wi-Fi 802.11ac' || select_network == 'Wi-Fi 802.11ax')
    {
        optionDirection = '<option value="upstream">Upstream</option>'+
                          '<option value="downstream">Downstream</option>';
        optionProfile =   '<option value="periodic">Periodic</option>'+
                          '<option value="cbr">CBR</option>'+
                          '<option value="vbr">VBR</option>';    
       
       // num_devices.placeholder = "max 22"; 
        dist_devices_gateway.placeholder = "max 50";
        //set a default value to battery capacity depending on a network
        load_freq.value = "1"; 
        tx_current.value = "107";
        rx_current.value = "40";
        idle_current.value = "1";
        battery_cap.value = "2400"; 
        voltage.value = "3"; 
        packetSizeShow("Wi-Fi");

    }
    else if (select_network == 'LoRaWAN')
    {
        optionDirection = '<option selected value="upstream">Upstream</option>';
        optionProfile = '<option selected value="periodic">Periodic</option>';  
       // num_devices.placeholder = "max 70000";    
        dist_devices_gateway.placeholder = "max 8000"; 

        packet_size_wifi.style.display = "none";
        lbl_packet_size_wifi.style.display = "none";
        packet_size_6lowpan.style.display = "none";
        lbl_packet_size_6lowpan.style.display = "none";
        packet_size_lorawan.style.display = "inherit";
        lbl_packet_size_lorawan.style.display = "inherit";
        load_freq.style.display = "inherit";
        lbl_load_freq.style.display = "inherit";

        //set a default value to battery capacity depending on a network
        tx_current.value = "77";
        rx_current.value = "28";
        idle_current.value = "1";
        sleep_current.value = "0.01";
        load_freq.value = "360"; 
        battery_cap.value = "1000"; 
        voltage.value = "3";    
        packetSizeShow("LoRaWAN");     
    }
    else if (select_network == '6LoWPAN')
    {
        optionDirection = '<option selected value="upstream">Upstream</option>';
        optionProfile = '<option selected value="periodic">Periodic</option>';  
       // num_devices.placeholder = "max 70000";    
        dist_devices_gateway.placeholder = "max 500"; 

        packet_size_wifi.style.display = "none";
        lbl_packet_size_wifi.style.display = "none";
        packet_size_lorawan.style.display = "none";
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_6lowpan.style.display = "inherit";
        lbl_packet_size_6lowpan.style.display = "inherit";
        load_freq.style.display = "inherit";
        lbl_load_freq.style.display = "inherit";

        //set a default value to battery capacity depending on a network
        tx_current.value = "7";
        rx_current.value = "1.5";
        idle_current.value = "0.5";
        load_freq.value = "10"; 
        battery_cap.value = "2400"; 
        voltage.value = "3";    
        packetSizeShow("6LoWPAN");     
    }
    else if (select_network == 'Wi-Fi HaLow')
    {
        optionDirection = '<option value="upstream">Upstream</option>'+
                          '<option value="downstream">Downstream</option>';
        optionProfile =   '<option value="periodic">Periodic</option>'+
                          '<option value="cbr">CBR</option>';    
       
       // num_devices.placeholder = "max 22"; 
        dist_devices_gateway.placeholder = "max 2000";
        //set a default value to battery capacity depending on a network
        load_freq.value = "1"; 
        num_devices.value = "5";
        battery_cap.value = "2400"; 
        voltage.value = "3"; 
        tx_current.value = "7.2";
        rx_current.value = "4.4";
        idle_current.value = "1";
        packetSizeShow("Wi-Fi");

    }
    else
    {
        num_devices.placeholder ="";
        dist_devices_gateway.placeholder = "";
        //diagra.SetAttribute('src', '../static/img/network-IOT_640.png');
        packetSizeShow("");   
    }
    direction.innerHTML = optionDirection;
    traffic_profile.innerHTML = optionProfile;
}

function onChangeSelectDirection(){
    var select_direction = direction.value;
    console.log("selected direction: "+select_direction);
    switch(select_direction)
    {
        case 'upstream' :
                //diagra.SetAttribute('src', '../static/img/diagram_traffic_upstream.png');
                break;
        case 'downstream' :
                //diagra.SetAttribute('src', '../static/img/diagram_traffic_downstream.png');
                break;
        default :
                //diagra.SetAttribute('src', '../static/img/network-IOT_640.png');
    }        
}  

function onChangeSelectTrafficProfile(){
    onChangeTrafficProfile();
}

function onChangeTrafficProfile(){
    var select_trafficProfile = traffic_profile.value;
    console.log("selected profile : "+select_trafficProfile);
    switch(select_trafficProfile) {
        case 'periodic' :
            if (network.value=="LoRaWAN") {
                packet_size_wifi.style.display = "none";
                lbl_packet_size_wifi.style.display = "none";
                packet_size_6lowpan.style.display = "none";
                lbl_packet_size_6lowpan.style.display = "none";
                packet_size_lorawan.style.display = "inherit";
                lbl_packet_size_lorawan.style.display = "inherit";
                load_freq.value = "360";
            }
            if (network.value=="6LoWPAN") {
                packet_size_wifi.style.display = "none";
                lbl_packet_size_wifi.style.display = "none";
                packet_size_lorawan.style.display = "none";
                lbl_packet_size_lorawan.style.display = "none";
                packet_size_6lowpan.style.display = "inherit";
                lbl_packet_size_6lowpan.style.display = "inherit";
                load_freq.value = "1";
            }
            if (network.value =='Wi-Fi 802.11ac' || network.value == 'Wi-Fi 802.11ax' || network.value == 'Wi-Fi HaLow') {
                packet_size_wifi.style.display = "inherit";
                lbl_packet_size_wifi.style.display = "inherit";
                packet_size_lorawan.style.display = "none";
                lbl_packet_size_lorawan.style.display = "none";
                packet_size_6lowpan.style.display = "none";
                lbl_packet_size_6lowpan.style.display = "none";
                load_freq.value = "1";
            }
                load_freq.style.display = "inherit";
                lbl_load_freq.style.display = "inherit";
                mean_load.style.display = "none";
                lbl_fps.style.display = "none";
                fps.style.display = "none";
                lbl_mean.style.display = "none";
                mean.style.display = "none";
                lbl_variance.style.display = "none";
                variance.style.display = "none";
                lbl_mean_load.style.display = "none";
                break;
        case 'cbr' :
                load_freq.style.display = "none";
                lbl_load_freq.style.display = "none";
                packet_size_wifi.style.display = "inherit";
                lbl_packet_size_wifi.style.display = "inherit";
                mean_load.style.display = "inherit";
                lbl_fps.style.display = "none";
                fps.style.display = "none";
                lbl_mean.style.display = "none";
                mean.style.display = "none";
                lbl_variance.style.display = "none";
                variance.style.display = "none";
                lbl_mean_load.style.display = "inherit";
                break;
        case 'vbr' :
                load_freq.style.display = "none";
                packet_size_wifi.style.display = "none";
                lbl_packet_size_wifi.style.display = "none";
                lbl_load_freq.style.display = "none";
                mean_load.style.display = "none";
                lbl_mean_load.style.display = "none";
                lbl_fps.style.display = "inherit";
                fps.style.display = "inherit";
                lbl_mean.style.display = "inherit";
                mean.style.display = "inherit";
                lbl_variance.style.display = "inherit";
                variance.style.display = "inherit";
                break;
        default :
                load_freq.style.display = "none";
                lbl_load_freq.style.display = "none";
                mean_load.style.display = "none";
                lbl_fps.style.display = "none";
                fps.style.display = "none";
                lbl_mean.style.display = "none";
                mean.style.display = "none";
                lbl_variance.style.display = "none";
                variance.style.display = "none"
                lbl_mean_load.style.display = "none";
    }
}  