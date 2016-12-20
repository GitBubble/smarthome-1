<?php
class Obj {
  function post() {
    $num = 0;
    if(isset($_POST['num']) && is_numeric($_POST['num']) && $_POST['num'] > 0) {
      $num = $_POST['num'];
    }

    $on = $_POST['light'];

    $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=light light='. $on .' num='. $num));

    return $return;
  }
}
?>
