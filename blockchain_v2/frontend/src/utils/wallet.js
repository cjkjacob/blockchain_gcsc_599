import { sha256 } from 'js-sha256'
import { ec as EC } from 'elliptic'

const ec = new EC('secp256k1')

export function signEffort(effortData, privateKeyHex) {
  const key = ec.keyFromPrivate(privateKeyHex)
  const hash = sha256(JSON.stringify(effortData))
  const signature = key.sign(hash)
  return signature.toDER('hex')
}

export function getPublicKeyFromPrivate(privateKeyHex) {
  return ec.keyFromPrivate(privateKeyHex).getPublic('hex')
}
