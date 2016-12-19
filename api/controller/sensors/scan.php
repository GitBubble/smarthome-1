<?php
class Obj {
  function get() {
    $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=sensor do=scan'));

    return [
      'content' => $return,
      'status' => 200
    ];
  }
}
?>
