<?php
class Obj {
  function post() {
    $return = json_decode(shell_exec('python ../services/sonos/app.py mode=speaker do=mute ip='. $_POST['ip']));

    if($return->status == 200) {
      $mongo = new MongoDB\Client("mongodb://". MONGODB_IP .":". MONGODB_PORT);
      $collection = $mongo->smarthome->home_audios;

      $collection->updateOne([
        'uniqueid' => $return->uniqueid
      ],[
        '$set' => [
          'control.mute' => $return->mute,
          'updated_at' => new MongoDB\BSON\UTCDateTime(),
        ]
      ]);
    }
    
    return $return;
  }
}
?>
