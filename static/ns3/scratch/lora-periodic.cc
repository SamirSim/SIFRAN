#include "ns3/end-device-lora-phy.h"
#include "ns3/gateway-lora-phy.h"
#include "ns3/class-a-end-device-lorawan-mac.h"
#include "ns3/gateway-lorawan-mac.h"
#include "ns3/simulator.h"
#include "ns3/log.h"
#include "ns3/constant-position-mobility-model.h"
#include "ns3/okumura-hata-propagation-loss-model.h"
#include "ns3/cost231-propagation-loss-model.h"
#include "ns3/hybrid-buildings-propagation-loss-model.h"
#include "ns3/lora-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/node-container.h"
#include "ns3/mobility-module.h"
#include "ns3/position-allocator.h"
#include "ns3/periodic-sender-helper.h"
#include "ns3/command-line.h"
#include "ns3/basic-energy-source-helper.h"
#include "ns3/lora-radio-energy-model-helper.h"
#include "ns3/file-helper.h"
#include "ns3/names.h"
#include "ns3/core-module.h"
#include "ns3/buildings-helper.h"
#include "ns3/building.h"
#include <algorithm>
#include <ctime>
#include <iomanip>
#include <fstream>
#include <iostream>
#include "ns3/string.h"

using namespace ns3;
using namespace lorawan;

void PrintPositions (NodeContainer loraNodes)
{
  
    Ptr<RandomWalk2dMobilityModel> mob = loraNodes.Get(1)->GetObject<RandomWalk2dMobilityModel>();
    Vector pos = mob->GetPosition ();
    std::cout << "POS: x=" << pos.x << ", y=" << pos.y << ", z=" << pos.z << "," << Simulator::Now ().GetSeconds ()<< std::endl;
    //mob->SetVelocity (Vector(1,0,0));
    
    Simulator::Schedule(Seconds(1), &PrintPositions, loraNodes);
}

NS_LOG_COMPONENT_DEFINE ("lora-periodic");

int
main (int argc, char *argv[]) {
  /*/ Defining input parameters /*/
  // Simulation Time Seconds
  double simulationTime = 100;
  // Number of stations
  int nSta = 400;
  // Number of gatewyas
  int nGW = 1;
  // Spreading Factor
  double SF=0; // If SF=0, then the SF is set automatically
  // Coding Rate
  uint8_t codingRate=1;
  // Cyclic Redundancy Check
  int crc = 0;
  // Payload size in bytes
  double payloadSize = 10;
  // Packet period in seconds
  int period = 60;
  // Meters between GW and stations
  double distance = 500;
  // Traffic Type (Confirmed or Unconfirmed)
  std::string trafficType = "Unconfirmed";
  // Channel Width (MHz)
  int channelWidth = 80;
  // Delay Propagation Delay
  std::string propDelay = "ConstantSpeedPropagationDelayModel";
  // Radio environment
  std::string radioEnvironment = "Rural";

  bool energyRatio = true;
  bool successRate = false;
  bool mobileNodes = false;

  //Energy parameters
  // Tx current draw in mA
  double txCurrent = 77;
  // Rx current draw in mA
  double rxCurrent = 28;
  // CCA_Busy current draw in mA
  double sleepCurrent = 0.001;
  // Idle current draw in mA
  double standByCurrent = 1;
  // Battery Voltage
  double voltage = 3; // in V

  CommandLine cmd;
  cmd.AddValue ("nSta", "Number of end devices to include in the simulation", nSta);
  cmd.AddValue ("nGW", "Number of gateways", nGW);
  cmd.AddValue ("distance", "The distance of the area to simulate", distance);
  cmd.AddValue ("SF", "Fixed spreading factor", SF);
  cmd.AddValue ("voltage", "voltage in Volts", voltage);
  cmd.AddValue ("codingRate", "Coding Rate", codingRate);
  cmd.AddValue ("mobileNodes", "Mobile nodes or not", mobileNodes);
  cmd.AddValue ("crc", "Cyclic Redundancy Check", crc);
  cmd.AddValue ("trafficType", "Confirmed or unconfirmed traffic", trafficType);
  cmd.AddValue ("simulationTime", "The time for which to simulate", simulationTime);
  cmd.AddValue ("payloadSize", "The size of the payload", payloadSize);
  cmd.AddValue ("period", "The period in seconds to be used by periodically transmitting applications", period);
  cmd.AddValue ("channelWidth", "Channel Width in MHz", channelWidth);
  cmd.AddValue ("propDelay", "Delay Propagation Model", propDelay);
  cmd.AddValue ("radioEnvironment", "Distance Propagation Model", radioEnvironment);
  cmd.AddValue ("energyRatio", "Energy ratio in Joules/Byte", energyRatio);
  cmd.AddValue ("successRate", "Percentage of successful packets", successRate);
  cmd.AddValue ("txCurrent", "Percentage of successful packets", txCurrent);
  cmd.AddValue ("rxCurrent", "Percentage of successful packets", rxCurrent);
  cmd.AddValue ("sleepCurrent", "Percentage of successful packets", sleepCurrent);
  cmd.AddValue ("standByCurrent", "Percentage of successful packets", standByCurrent);
  //cmd.AddValue ("topologyFile", "Topology file name", topologyFile);
  cmd.Parse (argc, argv);

  distance = distance / nGW;
  nSta = (int) (nSta / nGW) + 1;

  if (energyRatio) {
    LogComponentEnable ("lora-periodic", LOG_LEVEL_ALL);
    LogComponentEnable ("LoraRadioEnergyModel", LOG_LEVEL_ALL);
    LogComponentEnable ("EndDeviceLorawanMac", LOG_LEVEL_ALL);
    LogComponentEnable ("GatewayLorawanMac", LOG_LEVEL_ALL);
    LogComponentEnable ("LoraPhy", LOG_LEVEL_ALL);
  }

  LogComponentEnableAll (LOG_PREFIX_FUNC);
  LogComponentEnableAll (LOG_PREFIX_NODE);
  LogComponentEnableAll (LOG_PREFIX_TIME);

  // Mobility
  MobilityHelper mobility;

  if (mobileNodes) {
     mobility.SetPositionAllocator ("ns3::UniformDiscPositionAllocator", "rho", DoubleValue (distance),
                                 "X", DoubleValue (0.0), "Y", DoubleValue (0.0), "Z", DoubleValue(1.0));

      mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                                "Mode", StringValue ("Time"),
                                "Time", StringValue (std::to_string(simulationTime)),
                                "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=20.0]"),
                                "Bounds", RectangleValue (Rectangle (-distance, distance, -distance, distance)));
  } 
  else {
    mobility.SetPositionAllocator ("ns3::UniformDiscPositionAllocator", "rho", DoubleValue (distance),
                                 "X", DoubleValue (0.0), "Y", DoubleValue (0.0), "Z", DoubleValue(1.0));
    mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  }

  Ptr<LoraChannel> channel;
  Ptr<PropagationDelayModel> delay = CreateObject<ConstantSpeedPropagationDelayModel> ();

  if (radioEnvironment == "Suburban") {
    Ptr<LogDistancePropagationLossModel> loss = CreateObject<LogDistancePropagationLossModel> ();
    channel = CreateObject<LoraChannel> (loss, delay);
  } else if (radioEnvironment == "Urban") {
    Ptr<Cost231PropagationLossModel> loss = CreateObject<Cost231PropagationLossModel> ();
    channel = CreateObject<LoraChannel> (loss, delay);
  } else if (radioEnvironment == "Rural") {
    Ptr<OkumuraHataPropagationLossModel> loss = CreateObject<OkumuraHataPropagationLossModel> ();
    channel = CreateObject<LoraChannel> (loss, delay);;
  } else if (radioEnvironment == "Indoor") {
    Ptr<HybridBuildingsPropagationLossModel> loss = CreateObject<HybridBuildingsPropagationLossModel> ();
    channel = CreateObject<LoraChannel> (loss, delay);
  }

  // Installing phy & mac layers on the overloading stations
  LoraPhyHelper phyHelper = LoraPhyHelper ();
  phyHelper.SetChannel (channel);

  // Create the LorawanMacHelper
  LorawanMacHelper macHelper = LorawanMacHelper ();

  // Create the LoraHelper
  LoraHelper helper = LoraHelper ();
  helper.EnablePacketTracking (); // Output filename

  // Create a set of nodes
  NodeContainer endDevices;
  endDevices.Create (nSta);

  // Assign a mobility model to each node
  mobility.Install (endDevices);

  //PrintPositions (endDevices);

  // Create the LoraNetDevices of the end devices
  phyHelper.SetDeviceType (LoraPhyHelper::ED);
  macHelper.SetDeviceType (LorawanMacHelper::ED_A);
  NetDeviceContainer endDevicesNetDevices = helper.Install (phyHelper, macHelper, endDevices);

  // Create the gateway nodes (allocate them uniformely on the disc)
  NodeContainer gateways;
  gateways.Create (1);

  Ptr<ListPositionAllocator> allocator = CreateObject<ListPositionAllocator> ();
  // Make it so that nodes are at a certain height > 0
  MobilityHelper mobilityGW;
  allocator->Add (Vector (0.0, 0.0, 50.0));
  mobilityGW.SetPositionAllocator (allocator);
  mobilityGW.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobilityGW.Install (gateways);

  if (radioEnvironment == "Indoor") {
      double x_min = 0.0;
      double x_max = 10.0;
      double y_min = 0.0;
      double y_max = 20.0;
      double z_min = 0.0;
      double z_max = 10.0;
      Ptr<Building> b = CreateObject <Building> ();
      b->SetBoundaries (Box (x_min, x_max, y_min, y_max, z_min, z_max));
      b->SetBuildingType (Building::Residential);
      b->SetExtWallsType (Building::ConcreteWithWindows);
      b->SetNFloors (3);
      b->SetNRoomsX (3);
      b->SetNRoomsY (2);

      BuildingsHelper::Install (endDevices);
      
      BuildingsHelper::Install (gateways);
    }

  // Create a netdevice for each gateway
  phyHelper.SetDeviceType (LoraPhyHelper::GW);
  macHelper.SetDeviceType (LorawanMacHelper::GW);
  helper.Install (phyHelper, macHelper, gateways);

  macHelper.SetSpreadingFactorsUp (endDevices, gateways, channel, SF, codingRate, crc, trafficType);

  NS_LOG_DEBUG ("Completed configuration");

  /*/ Setting traffic applications /*/
  Time appStopTime = Seconds (simulationTime);
  PeriodicSenderHelper appHelper = PeriodicSenderHelper ();
  appHelper.SetPeriod (Seconds (period));
  appHelper.SetPacketSize (payloadSize);
  ApplicationContainer appContainer = appHelper.Install (endDevices);

  /*/ Installing energy models /*/
  if (energyRatio) {    
    BasicEnergySourceHelper basicSourceHelper;
    LoraRadioEnergyModelHelper radioEnergyHelper;

    // configure energy source
    basicSourceHelper.Set ("BasicEnergySourceInitialEnergyJ", DoubleValue (10000)); // Energy in Joules
    basicSourceHelper.Set ("BasicEnergySupplyVoltageV", DoubleValue (voltage));

    radioEnergyHelper.Set ("StandbyCurrentA", DoubleValue (standByCurrent/1000));
    radioEnergyHelper.Set ("TxCurrentA", DoubleValue (txCurrent/1000));
    radioEnergyHelper.Set ("SleepCurrentA", DoubleValue (sleepCurrent/1000));
    radioEnergyHelper.Set ("RxCurrentA", DoubleValue (rxCurrent/1000));

    radioEnergyHelper.SetTxCurrentModel ("ns3::LinearLoraTxCurrentModel");

    // install source on EDs' nodes
    EnergySourceContainer sources = basicSourceHelper.Install (endDevices);
    Names::Add ("/Names/EnergySource", sources.Get (0));

    // install device model
    DeviceEnergyModelContainer deviceModels = radioEnergyHelper.Install (endDevicesNetDevices, sources);
  }
  
  Simulator::Stop (appStopTime);

  NS_LOG_INFO ("Running simulation...");

  Simulator::Run ();

  Simulator::Destroy ();

  LoraPacketTracker &tracker = helper.GetPacketTracker ();

  std::cout << std::fixed;
  std::cout << std::setprecision(2);

  /*/ Gatherting KPIs /*/
  std::cout << "Success rate: " << std::to_string(tracker.CountMacPacketsGlobally (Seconds (0), appStopTime)) << std::endl;
  std::cout << "Throughput: " << std::to_string((tracker.CountMacPacketsReceived (Seconds (0), appStopTime)*payloadSize*8)/simulationTime/1024) << std::endl; // kbps

  return 0;
}

/*
  CsvReader csv (topologyFile);

    while (csv.FetchNextRow ()) {
        if (csv.IsBlankRow ()) {
          continue;
        }    
        // Read the trace and get the arrival information
      double x, y, z;
      bool ok1, ok2, ok3;
      ok1 = csv.GetValue (0, x);
      ok2= csv.GetValue (1, y);
      ok3 = csv.GetValue (2, z);
      
      for (uint32_t i = 0; i < nSta; i++) {
        csv.FetchNextRow ();
        ok1 = csv.GetValue (0, x);
        ok2= csv.GetValue (1, y);
        ok3 = csv.GetValue (2, z);
        positionAlloc->Add (Vector (x, y, z));
        //std::cout << x << " and " << y << " and " << z << std::endl;
      }
      mobility.SetPositionAllocator (positionAlloc);
      mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
      mobility.Install(endDevices);

      for (uint32_t i = 0; i < nGW; i++) {
        csv.FetchNextRow ();
        ok1 = csv.GetValue (0, x);
        ok2= csv.GetValue (1, y);
        ok3 = csv.GetValue (2, z);
        positionGW->Add (Vector (x, y, z));
        //std::cout << x << " AP and " << y << " and " << z << std::endl;
      }
    
      mobility.SetPositionAllocator (positionGW);
      mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
      mobility.Install(gateways);
      break;
    }
  */