function zeroFill(number, width) {
  width -= number.toString().length;
  if (width > 0) {
    return new Array(width + (/\./.test(number) ? 2 : 1)).join("0") + number;
  }
  return number + "";
}

function int64(low, hi) {
  this.low = low >>> 0;
  this.hi = hi >>> 0;
  this.backing = null;
}

int64.prototype.add32inplace = function (val) {
  let new_lo = (((this.low >>> 0) + val) & 0xffffffff) >>> 0;
  let new_hi = this.hi >>> 0;
  if (new_lo < this.low) new_hi++;
  this.hi = new_hi;
  this.low = new_lo;
  if (this.backing !== null) {
    if (this.backing.byteLength < val) throw new Error("int64.add32inplace: overflow");
    this.backing = new Uint8Array(this.backing.buffer, val, this.backing.byteLength - val);
  }
};

int64.prototype.add32 = function (val) {
  let new_lo = (((this.low >>> 0) + val) & 0xffffffff) >>> 0;
  let new_hi = this.hi >>> 0;
  if (new_lo < this.low) new_hi++;
  let ret = new int64(new_lo, new_hi);
  if (this.backing !== null) {
    if (this.backing.byteLength < val) throw new Error("int64.add32: overflow");
    ret.backing = new Uint8Array(this.backing.buffer, val, this.backing.byteLength - val);
  }
  return ret;
};

int64.prototype.sub32 = function (val) {
  let new_lo = (((this.low >>> 0) - val) & 0xffffffff) >>> 0;
  let new_hi = this.hi >>> 0;
  if ((new_lo > this.low) & 0xffffffff) new_hi--;
  return new int64(new_lo, new_hi);
};

int64.prototype.sub32inplace = function (val) {
  let new_lo = (((this.low >>> 0) - val) & 0xffffffff) >>> 0;
  let new_hi = this.hi >>> 0;
  if ((new_lo > this.low) & 0xffffffff) new_hi--;
  this.hi = new_hi;
  this.low = new_lo;
};

int64.prototype.and32 = function (val) {
  return new int64(this.low & val, this.hi);
};

int64.prototype.and64 = function (vallo, valhi) {
  return new int64(this.low & vallo, this.hi & valhi);
};

int64.prototype.toString = function (radix = 16) {
  let lo_str = (this.low >>> 0).toString(radix);
  let hi_str = (this.hi >>> 0).toString(radix);
  if (this.hi == 0) return lo_str;
  const width = radix === 16 ? 8 : Math.ceil(32 / Math.log2(radix));
  lo_str = zeroFill(lo_str, width);
  return hi_str + lo_str;
};

globalThis.int64 = int64;
export { int64 };
export default int64;