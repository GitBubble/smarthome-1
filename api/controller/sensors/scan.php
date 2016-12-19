<?php
class Obj {
  function get() {
    $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=sensor do=scan'));

    if(count($return) > 0) {
      foreach($return AS $key => $val) {
        $mongo = new MongoDB\Client("mongodb://". MONGODB_IP .":". MONGODB_PORT);
        $collection = $mongo->smarthome->sensors;

        $document = $collection->findOne([
          'uniqueid' => $val->uniqueid
        ]);

        if(isset($document['_id'])) {
          $collection->updateOne([
            'uniqueid' => $val->uniqueid
          ],[
            '$set' => [
              'battery' => $val->battery,
              'sensors' => $val->sensors,
              'updated_at' => new MongoDB\BSON\UTCDateTime(),
            ]
          ]);
        } else {
          $collection->insertOne([
            'uniqueid' => $val->uniqueid,
            'battery' => $val->battery,
            'sensors' => $val->sensors,
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
        'content' => 'There are none sensor founds right now!',
        'status' => 404
      ];
    }
  }
}
?>