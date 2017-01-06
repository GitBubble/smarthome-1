<?php
class Obj {
  function get() {
    $return = json_decode(shell_exec('python ../services/sonos/app.py mode=speaker do=scan'));

    if(count($return) > 0) {
      $mongo = new MongoDB\Client("mongodb://". MONGODB_IP .":". MONGODB_PORT);
      $collection = $mongo->smarthome->home_audios;

      foreach($return AS $key => $val) {
        $document = $collection->findOne([
          'uniqueid' => $val->uniqueid
        ]);

        if(isset($document['_id'])) {
          $collection->updateOne([
            'uniqueid' => $val->uniqueid
          ],[
            '$set' => [
              'ip' => $key,
              'name' => $val->name,
              'device' => [
                'brand' => 'Sonos',
                'modelid' => $val->model_name,
                'software_version' => $val->software_version,
                'hardware_version' => $val->hardware_version,
              ],
              'network' => [
                'ip' => $val->ip_address,
                'mac_address' => $val->mac_address,
              ],
              'control' => [
                'status_light' => $val->status_light,
                'volume' => $val->volume,
                'mute' => $val->mute,
              ],
              'updated_at' => new MongoDB\BSON\UTCDateTime(),
            ]
          ]);
        } else {
          $collection->insertOne([
            'uniqueid' => $val->uniqueid,
            'name' => $val->name,
            'device' => [
              'brand' => 'Sonos',
              'modelid' => $val->model_name,
              'software_version' => $val->software_version,
              'hardware_version' => $val->hardware_version,
            ],
            'network' => [
              'ip' => $val->ip_address,
              'mac_address' => $val->mac_address,
            ],
            'control' => [
              'status_light' => $val->status_light,
              'volume' => $val->volume,
              'mute' => $val->mute,
            ],
            'updated_at' => new MongoDB\BSON\UTCDateTime(),
            'created_at' => new MongoDB\BSON\UTCDateTime(),
          ]);
        }
      }

      return [
        'content' => $return,
        'status' => 200
      ];
    } else {
      return [
        'content' => 'There are none home audio systems founds right now!',
        'status' => 404
      ];
    }
  }
}
?>
