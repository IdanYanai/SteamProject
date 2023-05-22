SIZE_HEADER_FORMAT = "00000|"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)


def recv_by_size(sock):
    size_header = b''
    data_len = 0
    while len(size_header) < size_header_size:
        _s = sock.recv(size_header_size - len(size_header))
        if _s == b'':
            break
        else:
            size_header += _s
    data = b''
    if size_header != b'':
        data_len = int(size_header[:size_header_size - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if _d == b'':
                break
            else:
                data += _d

    if data_len != len(data):
        data = b''  # Partial data is like no data !
    return data   # ( or data.decode() if want it as string)


def send_with_size(sock, bdata):
    len_data = len(bdata)
    header_data = str(len(bdata)).zfill(size_header_size - 1) + "|"

    bytea = bytearray(header_data, encoding='utf8') + bdata

    sock.send(bytea)

