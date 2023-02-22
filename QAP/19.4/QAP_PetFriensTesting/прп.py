abc = {
  "key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729"
}
auth_key = abc['key']
new_auth_key = auth_key[0:-4] + 'b7gh'
print(new_auth_key)