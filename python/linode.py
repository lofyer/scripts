import linode

a=linode.Api("ueVfhwdTiYEuiwwwMXbj79H6o3vf1x7pcMcXxAX7myctbcYJ5mTGQ5QTmFm4w7nc")

linode.params.get_required_params(a.endpoint)

a.linode.list()
