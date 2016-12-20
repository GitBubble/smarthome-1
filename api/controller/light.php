<?php
class Obj {
  function post() {
    $num = 0;
    if(isset($_POST['num']) && is_numeric($_POST['num']) && $_POST['num'] > 0) {
      $num = $_POST['num'];
    }

    if(isset($_POST['light']) && ($_POST['light'] == 'on' || $_POST['light'] == 'off')) {
      $on = $_POST['light'];

      $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=light light='. $on .' num='. $num));
      if(count($return) > 0) {
        $mongo = new MongoDB\Client("mongodb://". MONGODB_IP .":". MONGODB_PORT);
        $collection = $mongo->smarthome->light_log;

        foreach($return AS $key => $val) {
          if($val->status == 200) {
            $collection->insertOne([
              'uniqueid' => $val->uniqueid,
              'swversion' => $val->swversion,
              'state' => $val->state,
              'num' => $val->num,
              'modelid' => $val->modelid,
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
          'content' => _('There are none lights found right now.'),
          'status' => 404
        ];
      }
    } else {
      return [
        'content' => _('You need to tell what shut happen with the light.'),
        'status' => 404
      ];
    }
  }
}
?>
