export default class Currency {
  constructor(code, name) {
    if (typeof (code) === 'string') {
      this.__code = code;
    } else {
      throw new Error(TypeError('code must be a String'));
    }

    if (typeof (name) === 'string') {
      this.__name = name;
    } else {
      throw new Error(TypeError('name must be a String'));
    }
  }

  set code(value) {
    if (typeof (code) === 'string') {
      this.__code = value;
    } else {
      throw new Error(TypeError('code must be a String'));
    }
  }

  get code() {
    return this.__code;
  }

  set name(value) {
    if (typeof (value) === 'string') {
      this.__name = value;
    } else {
      throw new Error(TypeError('name must be a String'));
    }
  }

  get name() {
    return this.__name;
  }

  displayFullCurrency() {
    return `${this.name} (${this.code})`;
  }
}
