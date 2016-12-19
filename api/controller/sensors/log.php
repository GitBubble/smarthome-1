<?php
class Obj {
  function post() {
    if(isset($_POST['num']) && is_numeric($_POST['num'])) {
      $sensor_num = $_POST['num'];
    } else {
      return [
        'status' => 404,
        'error' => 'Need a sensor number to track.'
      ];
    }

    $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=sensor do=get num='. $sensor_num));

    if(!isset($return->uniqueid)) {
      return [
        'status' => 404,
        'error' => 'Sensor '. $sensor_num .' not available.'
      ];
    } else {
      $mongo = new MongoDB\Client("mongodb://". MONGODB_IP .":". MONGODB_PORT);
      $collection = $mongo->smarthome->sensor_log;

      $collection->insertOne([
        'uniqueid' => $return->uniqueid,
        'modelid' => $return->modelid,
        'swversion' => $return->swversion,
        'created_at' => new MongoDB\BSON\UTCDateTime(),
        'type' => $return->type,
        'state' => [
          'value' => $return->state->value
        ]
      ]);

      return [
        'content' => $return,
        'status' => 200
      ];
    }
  }
}
?>
