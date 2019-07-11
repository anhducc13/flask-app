def wrap_response(data=None, message="", http_code=200, type_error=None):
    """
    Return general HTTP response
    :param data:
    :param str message: detail info
    :param int http_code:
    :param int type_error:
    :return:
    """
    res = {
        'code': http_code,
        'success': http_code // 100 == 2,
        'message': message,
        'data': data,
        'typeError': type_error
    }

    return res, http_code
