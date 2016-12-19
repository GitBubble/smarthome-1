<?php
class Obj {
  function get() {
    $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=light do=scan'));

    if(count($return) > 0) {
      $mongo = new MongoDB\Client("mongodb://". MONGODB_IP .":". MONGODB_PORT);
      $collection = $mongo->smarthome->lights;

      foreach($return AS $key => $val) {
        $document = $collection->findOne([
          'uniqueid' => $val->uniqueid
        ]);

        if(isset($document['_id'])) {
          $collection->updateOne([
            'uniqueid' => $val->uniqueid
          ],[
            '$set' => [
              'id' => $key,
              'swversion' => $val->swversion,
              'state' => $val->state,
              'updated_at' => new MongoDB\BSON\UTCDateTime(),
            ]
          ]);
        } else {
          $collection->insertOne([
            'id' => $key,
            'uniqueid' => $val->uniqueid,
            'modelid' => $val->modelid,
            'swversion' => $val->swversion,
            'state' => $val->state,
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
        'content' => 'There are none lights founds right now!',
        'status' => 404
      ];
    }
  }
}
?>
