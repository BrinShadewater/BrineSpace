const actions = new Set(['mine','collect','unload','blocked','power-on','power-off','charging','disabled']);
export class RoverMotion {
  constructor() {
    this.state = 'drive';
    this.heading = 'south';
    this.velocity = 0;
    this.wheelFrame = 0;
    this.actionTime = null;
    this.distance = 0;
    this.pending = null;
    this.cargoLoaded = false;
    this.deposited = 0;
    this.completed = false;
  }

  command(state, heading = this.heading) {
    if (state === this.state && heading === this.heading) {this.pending = null; return;}
    if (['collect','unload','blocked'].includes(this.state) && this.actionTime !== null && this.actionTime < 4) {
      this.pending = {state,heading}; return;
    }
    if (this.state === 'mine' && this.actionTime !== null && this.actionTime >= .5 && this.actionTime < 5.5) {
      this.pending = {state,heading};
      const frame = Math.floor(this.actionTime * 30);
      if (frame < 45) this.actionTime = (179-frame)/30;
      else if (frame < 135) this.actionTime = 4.5;
      return;
    }
    this.state = state;
    this.heading = heading;
    this.actionTime = null;
    this.pending = null;
    this.completed = false;
    if (state === 'carry') this.cargoLoaded = true;
  }

  replay() {
    this.velocity = 0;
    this.wheelFrame = 0;
    this.actionTime = null;
    this.distance = 0;
    this.pending = null;
    this.completed = false;
  }

  update(dt, cruiseSpeed) {
    const travel = ['drive', 'reverse', 'steer-left', 'steer-right','carry'].includes(this.state);
    const target = travel ? cruiseSpeed * (this.state === 'reverse' ? -1 : 1) : 0;
    const before = this.velocity;
    const acceleration = 50;
    const difference = target - before;
    const rampTime = Math.min(dt, Math.abs(difference) / acceleration);
    this.velocity = before + Math.sign(difference) * acceleration * rampTime;
    if (Math.abs(this.velocity - target) < 1e-8) this.velocity = target;
    const distance = (before + this.velocity) * .5 * rampTime + this.velocity * (dt - rampTime);
    this.distance += distance;
    this.wheelFrame = ((this.wheelFrame + distance / cruiseSpeed * 30) % 60 + 60) % 60;
    if (actions.has(this.state) && this.velocity === 0) {
      this.actionTime = (this.actionTime ?? 0) + (before === 0 ? dt : dt - rampTime);
      if (this.actionTime >= 119/30 && !this.completed && ['collect','unload','blocked'].includes(this.state)) {
        this.completed = true;
        if (this.state === 'collect') this.cargoLoaded = true;
        if (this.state === 'unload') {this.cargoLoaded = false; this.deposited++;}
      }
      if (this.pending && this.actionTime >= (this.state === 'mine' ? 5.5 : 4)) {
        const next = this.pending; this.pending = null; this.command(next.state,next.heading);
      }
    }
    const braking = before !== 0 && (target === 0 || Math.sign(before) !== Math.sign(target));
    return {
      distance,
      status: braking && this.velocity !== 0 ? 'Braking'
        : this.velocity === 0 ? this.state === 'mine' ? 'Working' : 'Stopped'
        : Math.abs(this.velocity) < Math.abs(target) ? 'Accelerating'
        : this.velocity < 0 ? 'Reversing' : 'Rolling',
    };
  }

  sample() {
    if (actions.has(this.state) && this.actionTime !== null) {
      const count = this.state === 'mine' ? 180 : ['collect','unload','blocked'].includes(this.state) ? 120 : 60;
      const n = Math.floor(this.actionTime*30);
      return {state:this.state,frame:['charging','disabled'].includes(this.state) ? n%count : Math.min(count-1,n)};
    }
    const state = this.state === 'idle' || actions.has(this.state) ? 'drive' : this.state;
    const phase = Math.floor(this.wheelFrame + 1e-8) % 60;
    return { state, frame: state === 'reverse' ? (60 - phase) % 60 : phase };
  }

  wheelSample() {
    return Math.floor(this.wheelFrame + 1e-8) % 60;
  }
}
