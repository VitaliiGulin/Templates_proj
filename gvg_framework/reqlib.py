
class ComReqMan:

    @staticmethod
    def parse_req_args(is_dat: str):
        ldic_ret = {}
        if is_dat:
            la_key_value = is_dat.split('&')
            for rec in la_key_value:
                l_key, l_val = rec.split('=')
                ldic_ret[l_key] = l_val
        return ldic_ret


class GetReqMan:

    @staticmethod
    def get_req_dict(environ):
        ls_args = environ['QUERY_STRING']
        ldic_res = ComReqMan.parse_req_args(ls_args)
        return ldic_res


class PostReqMan:

    @staticmethod
    def get_post_bytes(i_env) -> bytes:
        ls_con_len = i_env.get('CONTENT_LENGTH')
        li_con_len = int(ls_con_len) if ls_con_len else 0

        lbts_ret = i_env['wsgi.input'].read(li_con_len) if li_con_len > 0 else b''
        return lbts_ret

    def get_req_dict(self, i_env):
        lbts_post = self.get_post_bytes(i_env)
        ldic_res = {}

        if lbts_post:
            ls_data = lbts_post.decode(encoding='utf-8')
            ldic_res = ComReqMan.parse_req_args(ls_data)
        return ldic_res
