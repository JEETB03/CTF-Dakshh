/**
 * Caesar Cipher utility for encoding/decoding text.
 * Default shift is 3 (classic Caesar cipher).
 */

export function caesarEncrypt(text: string, shift: number = 3): string {
  return text
    .split("")
    .map((char) => {
      if (char.match(/[a-z]/)) {
        return String.fromCharCode(((char.charCodeAt(0) - 97 + shift) % 26) + 97);
      }
      if (char.match(/[A-Z]/)) {
        return String.fromCharCode(((char.charCodeAt(0) - 65 + shift) % 26) + 65);
      }
      return char;
    })
    .join("");
}

export function caesarDecrypt(text: string, shift: number = 3): string {
  return caesarEncrypt(text, 26 - shift);
}
