import aiohttp
import asyncio
import pyjuicenet
from os import environ

TOKEN=environ.get('JN_API_KEY')
if not TOKEN:
  raise Exception(
    "Set the environment variable JN_API_KEY to your JuiceNet API token. "\
    "You can find it here: https://home.juice.net/Manage")

async def main():
  async with aiohttp.ClientSession() as session:
    api = pyjuicenet.Api(TOKEN, session)
    devices = await api.get_devices()
    results=[]
    for charger in devices:
        await charger.update_state()
        results.append(
                {"device_name": charger.name, 
                 "device_id": charger.id, 
                 "device_type": "evse", 
                 "device_brand": "enelx", 
                 "device_model": "juicebox40 pro", 
                 "charge_time": charger.charge_time, 
                 "energy_added": charger.energy_added, 
                 "voltage": charger.voltage, 
                 "amps": charger.amps, 
                 "watts": charger.watts, 
                 "temperature_c": charger.temperature, 
                 "status": charger.status })
        #info = await api.get_info(charger)
        #print(f"info: {info}")
        #for car in info['cars']:
            #print(f"car id: {car['car_id']} description: {car['description']} make: {car['model_info']['make']} model: {car['model_info']['model']} year: {car['model_info']['year']}")
    for result in results:
        print(result)

asyncio.run(main())
