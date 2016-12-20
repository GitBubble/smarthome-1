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
