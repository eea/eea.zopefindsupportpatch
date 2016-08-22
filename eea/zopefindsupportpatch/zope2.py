import logging
from Acquisition import aq_base
from DateTime.DateTime import DateTime
from OFS.Folder import Folder
from OFS.FindSupport import FindSupport, td, p_name, absattr
from OFS.FindSupport import expr_match, mtime_match, role_match
from DocumentTemplate.DT_Util import Eval

log = logging.getLogger('eea.zope_find_support_patch')


def patched_ZopeFind(self, obj, obj_ids=None, obj_metatypes=None,
                     obj_searchterm=None, obj_expr=None,
                     obj_mtime=None, obj_mspec=None,
                     obj_permission=None, obj_roles=None,
                     search_sub=0,
                     REQUEST=None, result=None, pre=''):
    """Patched Zope Find interface"""
    if result is None:
        result=[]

        if obj_metatypes and 'all' in obj_metatypes:
            obj_metatypes=None

        if obj_mtime and type(obj_mtime)==type('s'):
            obj_mtime=DateTime(obj_mtime).timeTime()

        if obj_permission:
            obj_permission=p_name(obj_permission)

        if obj_roles and type(obj_roles) is type('s'):
            obj_roles=[obj_roles]

        if obj_expr:
            # Setup expr machinations
            md=td()
            obj_expr=(Eval(obj_expr), md, md._push, md._pop)

    base = aq_base(obj)

    if hasattr(base, 'objectItems'):
        try:    items=obj.objectItems()
        except: return result
    else:
        return result

    try: add_result=result.append
    except:
        raise AttributeError, `result`

    for id, ob in items:
        if pre: p="%s/%s" % (pre, id)
        else:   p=id

        dflag=0
        if hasattr(ob, '_p_changed') and (ob._p_changed == None):
            dflag=1

        bs = aq_base(ob)
        if (hasattr(ob, 'PrincipiaSearchSource') and
                isinstance(ob.PrincipiaSearchSource(), unicode)) or (
                hasattr(ob, 'SearchableText') and
                isinstance(ob.SearchableText(), unicode)):
            searchterm = str(obj_searchterm).decode('utf-8')
        else:
            searchterm = str(obj_searchterm)
        if (
            (not obj_ids or absattr(bs.getId()) in obj_ids)
            and
            (not obj_metatypes or (hasattr(bs, 'meta_type') and
             bs.meta_type in obj_metatypes))
            and
            (not obj_searchterm or
             (hasattr(ob, 'PrincipiaSearchSource') and
              ob.PrincipiaSearchSource().find(searchterm) >= 0
              )
             or
             (hasattr(ob, 'SearchableText') and
              ob.SearchableText().find(searchterm) >= 0)
             )
            and
            (not obj_expr or expr_match(ob, obj_expr))
            and
            (not obj_mtime or mtime_match(ob, obj_mtime, obj_mspec))
            and
            ( (not obj_permission or not obj_roles) or \
               role_match(ob, obj_permission, obj_roles)
            )
            ):
            add_result((p, ob))
            dflag=0

        if search_sub and (hasattr(bs, 'objectItems')):
            subob = ob
            sub_p = p
            patched_ZopeFind(self, subob, obj_ids, obj_metatypes,
                               obj_searchterm, obj_expr,
                               obj_mtime, obj_mspec,
                               obj_permission, obj_roles,
                               search_sub,
                               REQUEST, result, sub_p)
        if dflag: ob._p_deactivate()

    return result


def initialize(context):
    """ Patch OFS.FindSupport.PrincipiaFind """
    FindSupport.ZopeFind = patched_ZopeFind
    FindSupport.PrincipiaFind = patched_ZopeFind
    log.info("Patched 'OFS.FindSupport.ZopeFind and PrincipiaFind")
