<?php
class Obj {
  function post() {
    $return = [
      'method' => $_POST['method'],
      'value' => $_POST['value'],
    ];

    return [
      'content' => $return,
      'status' => 200
    ];
  }
}
?>
