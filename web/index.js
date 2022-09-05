const statusArea = document.getElementById("status-area");

for (var i = 1; i <= 4; i++) {
  for (var j = 1; j <= 4; j++) {
    time = document.getElementById(`num${i}-time${j}`);
    speed = document.getElementById(`num${i}-speed${j}`);

    time.max = 15;
    time.min = 2;
    time.step = 1;
    time.value = 5;

    speed.min = 180;
    speed.max = 1080;
    speed.step = 30;
    speed.value = 360;
  }
}

function generate() {
  const rounds = Array(4);
  for (var i = 1; i <= 4; i++) {
    var d = {};
    d.nums = Array(4);

    var numStr = document.getElementById(`num${i}-field`).value;
    if (numStr.length != 4) {
      statusArea.value = `Invalid input : ${numStr}`;
      return;
    }
    for (var numIdx = 0; numIdx < 4; numIdx++) {
      d.nums[numIdx] = parseInt(numStr.charAt(numIdx));
    }
    d.times = Array(4);
    d.speeds = Array(4);
    for (var j = 1; j <= 4; j++) {
      d.times[j - 1] = parseInt(
        document.getElementById(`num${i}-time${j}`).value
      );
      d.speeds[j - 1] = parseInt(
        document.getElementById(`num${i}-speed${j}`).value
      );
    }
    rounds[i - 1] = d;
  }
  console.table(rounds);
  eel.generate(rounds)(update);
}

function update(message) {
  statusArea.value = message;
}
