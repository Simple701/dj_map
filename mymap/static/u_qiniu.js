
/**
 * 上传凭证算法实现参考
 * 请注意External Resources项中引用的第三方CryptoJS库
 */
var genUpToken = function(accessKey, secretKey, putPolicy) {

    //SETP 2
    var put_policy = JSON.stringify(putPolicy);
    console && console.log("put_policy = ", put_policy);

    //SETP 3
    var encoded = base64encode(utf16to8(put_policy));
    console && console.log("encoded = ", encoded);

    //SETP 4
    var hash = CryptoJS.HmacSHA1(encoded, secretKey);
    var encoded_signed = hash.toString(CryptoJS.enc.Base64);
    console && console.log("encoded_signed=", encoded_signed)

    //SETP 5
    var upload_token = accessKey + ":" + safe64(encoded_signed) + ":" + encoded;
    console && console.log("upload_token=", upload_token)
    return upload_token;
};