"""
テンプレート (potx) にスライドレイアウトパターンを追加するスクリプト。
既存の 5 レイアウトに加え、33 種類の新レイアウトを OOXML 直接操作で追加する。
"""

import zipfile
import shutil
import os
import copy
import uuid
from lxml import etree

# ── 設定 ──
TEMPLATE_SRC = r"c:\work\Blog\Template\Copilot_Template_Public.potx"
TEMPLATE_DST = r"c:\work\Blog\Template\Copilot_Template_Public.potx"  # 上書き

# ── 定数 ──
SLIDE_W = 12192000  # EMU (13.333")
SLIDE_H = 6858000   # EMU (7.5")
EMU_INCH = 914400

# マージン
MARGIN_L = int(1.2 * EMU_INCH)   # 1097280
MARGIN_R = int(1.2 * EMU_INCH)
MARGIN_T = int(0.5 * EMU_INCH)
CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R  # ≈9997440

# テーマカラー (EMU 参照用)
# accent1=F4364C, accent2=C03BC4, accent3=0078D4, accent4=FFC000
# accent5=127A93, accent6=49C5B1, dk1=595959, lt2=F2F2F2

# ── 名前空間 ──
NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

NS_CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
NS_REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS_LAYOUT_TYPE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout'
NS_MASTER_TYPE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster'

def emu(inches):
    """インチ → EMU 変換"""
    return int(inches * EMU_INCH)

def uid():
    """ユニークID用 GUID"""
    return '{%s}' % str(uuid.uuid4()).upper()


# ───────────────────────────────────────────────
# XML ヘルパー
# ───────────────────────────────────────────────
def make_text_sp(sp_id, name, x, y, cx, cy, text, font_size=1400,
                 bold=False, color_hex=None, scheme_color=None,
                 alignment='l', font_name='Yu Gothic UI', anchor='t',
                 wrap='square', fill_hex=None, line_hex=None, line_w=None):
    """テキストボックス図形の XML Element を生成"""
    sp = etree.SubElement(etree.Element('dummy'), '{%s}sp' % NSMAP['p'])

    # nvSpPr
    nvSpPr = etree.SubElement(sp, '{%s}nvSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(sp_id))
    cNvPr.set('name', name)
    cNvSpPr = etree.SubElement(nvSpPr, '{%s}cNvSpPr' % NSMAP['p'])
    cNvSpPr.set('txBox', '1')
    etree.SubElement(nvSpPr, '{%s}nvPr' % NSMAP['p'])

    # spPr
    spPr = etree.SubElement(sp, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(x)); off.set('y', str(y))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(cx)); ext.set('cy', str(cy))
    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', 'rect')
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])

    if fill_hex:
        solidFill = etree.SubElement(spPr, '{%s}solidFill' % NSMAP['a'])
        srgb = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
        srgb.set('val', fill_hex)
    else:
        etree.SubElement(spPr, '{%s}noFill' % NSMAP['a'])

    if line_hex:
        ln = etree.SubElement(spPr, '{%s}ln' % NSMAP['a'])
        if line_w:
            ln.set('w', str(line_w))
        sfill = etree.SubElement(ln, '{%s}solidFill' % NSMAP['a'])
        srgb = etree.SubElement(sfill, '{%s}srgbClr' % NSMAP['a'])
        srgb.set('val', line_hex)

    # txBody
    txBody = etree.SubElement(sp, '{%s}txBody' % NSMAP['p'])
    bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % NSMAP['a'])
    bodyPr.set('wrap', wrap)
    bodyPr.set('anchor', anchor)
    bodyPr.set('lIns', '91440'); bodyPr.set('tIns', '45720')
    bodyPr.set('rIns', '91440'); bodyPr.set('bIns', '45720')
    etree.SubElement(txBody, '{%s}lstStyle' % NSMAP['a'])
    p_el = etree.SubElement(txBody, '{%s}p' % NSMAP['a'])
    pPr = etree.SubElement(p_el, '{%s}pPr' % NSMAP['a'])
    pPr.set('algn', alignment)
    r_el = etree.SubElement(p_el, '{%s}r' % NSMAP['a'])
    rPr = etree.SubElement(r_el, '{%s}rPr' % NSMAP['a'])
    rPr.set('lang', 'ja-JP')
    rPr.set('sz', str(font_size))
    if bold:
        rPr.set('b', '1')
    if color_hex:
        sf = etree.SubElement(rPr, '{%s}solidFill' % NSMAP['a'])
        sc = etree.SubElement(sf, '{%s}srgbClr' % NSMAP['a'])
        sc.set('val', color_hex)
    elif scheme_color:
        sf = etree.SubElement(rPr, '{%s}solidFill' % NSMAP['a'])
        sc = etree.SubElement(sf, '{%s}schemeClr' % NSMAP['a'])
        sc.set('val', scheme_color)
    latin = etree.SubElement(rPr, '{%s}latin' % NSMAP['a'])
    latin.set('typeface', font_name)
    ea = etree.SubElement(rPr, '{%s}ea' % NSMAP['a'])
    ea.set('typeface', font_name)
    t_el = etree.SubElement(r_el, '{%s}t' % NSMAP['a'])
    t_el.text = text

    return sp


def make_rect_sp(sp_id, name, x, y, cx, cy, fill_hex=None, scheme_fill=None,
                 line_hex=None, line_w=12700, rounded=False, opacity=None):
    """矩形図形の XML Element を生成"""
    sp = etree.SubElement(etree.Element('dummy'), '{%s}sp' % NSMAP['p'])

    nvSpPr = etree.SubElement(sp, '{%s}nvSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(sp_id))
    cNvPr.set('name', name)
    etree.SubElement(nvSpPr, '{%s}cNvSpPr' % NSMAP['p'])
    etree.SubElement(nvSpPr, '{%s}nvPr' % NSMAP['p'])

    spPr = etree.SubElement(sp, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(x)); off.set('y', str(y))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(cx)); ext.set('cy', str(cy))
    prst = 'roundRect' if rounded else 'rect'
    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', prst)
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])

    if fill_hex:
        solidFill = etree.SubElement(spPr, '{%s}solidFill' % NSMAP['a'])
        srgb = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
        srgb.set('val', fill_hex)
        if opacity is not None:
            alpha = etree.SubElement(srgb, '{%s}alpha' % NSMAP['a'])
            alpha.set('val', str(int(opacity * 1000)))
    elif scheme_fill:
        solidFill = etree.SubElement(spPr, '{%s}solidFill' % NSMAP['a'])
        sc = etree.SubElement(solidFill, '{%s}schemeClr' % NSMAP['a'])
        sc.set('val', scheme_fill)
        if opacity is not None:
            alpha = etree.SubElement(sc, '{%s}alpha' % NSMAP['a'])
            alpha.set('val', str(int(opacity * 1000)))
    else:
        etree.SubElement(spPr, '{%s}noFill' % NSMAP['a'])

    ln = etree.SubElement(spPr, '{%s}ln' % NSMAP['a'])
    ln.set('w', str(line_w))
    if line_hex:
        sfill = etree.SubElement(ln, '{%s}solidFill' % NSMAP['a'])
        srgb = etree.SubElement(sfill, '{%s}srgbClr' % NSMAP['a'])
        srgb.set('val', line_hex)
    else:
        etree.SubElement(ln, '{%s}noFill' % NSMAP['a'])

    return sp


def make_img_placeholder(sp_id, name, x, y, cx, cy):
    """画像プレースホルダー風の図形(枠線+アイコン)"""
    sp = etree.SubElement(etree.Element('dummy'), '{%s}sp' % NSMAP['p'])

    nvSpPr = etree.SubElement(sp, '{%s}nvSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(sp_id))
    cNvPr.set('name', name)
    etree.SubElement(nvSpPr, '{%s}cNvSpPr' % NSMAP['p'])
    etree.SubElement(nvSpPr, '{%s}nvPr' % NSMAP['p'])

    spPr = etree.SubElement(sp, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(x)); off.set('y', str(y))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(cx)); ext.set('cy', str(cy))
    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', 'rect')
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])

    solidFill = etree.SubElement(spPr, '{%s}solidFill' % NSMAP['a'])
    srgb = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
    srgb.set('val', 'E8ECF1')

    ln = etree.SubElement(spPr, '{%s}ln' % NSMAP['a'])
    ln.set('w', '12700')
    sfill = etree.SubElement(ln, '{%s}solidFill' % NSMAP['a'])
    srgb2 = etree.SubElement(sfill, '{%s}srgbClr' % NSMAP['a'])
    srgb2.set('val', 'C0C8D0')
    dash = etree.SubElement(ln, '{%s}prstDash' % NSMAP['a'])
    dash.set('val', 'dash')

    # 画像アイコンテキスト
    txBody = etree.SubElement(sp, '{%s}txBody' % NSMAP['p'])
    bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % NSMAP['a'])
    bodyPr.set('anchor', 'ctr')
    etree.SubElement(txBody, '{%s}lstStyle' % NSMAP['a'])
    p_el = etree.SubElement(txBody, '{%s}p' % NSMAP['a'])
    pPr = etree.SubElement(p_el, '{%s}pPr' % NSMAP['a'])
    pPr.set('algn', 'ctr')
    r_el = etree.SubElement(p_el, '{%s}r' % NSMAP['a'])
    rPr = etree.SubElement(r_el, '{%s}rPr' % NSMAP['a'])
    rPr.set('lang', 'ja-JP'); rPr.set('sz', '1800')
    sf = etree.SubElement(rPr, '{%s}solidFill' % NSMAP['a'])
    sc = etree.SubElement(sf, '{%s}srgbClr' % NSMAP['a'])
    sc.set('val', '8899AA')
    t_el = etree.SubElement(r_el, '{%s}t' % NSMAP['a'])
    t_el.text = '🖼'

    return sp


def make_line_sp(sp_id, name, x, y, cx, cy, color_hex='0078D4', line_w=19050):
    """線 (コネクタ) 図形"""
    sp = etree.SubElement(etree.Element('dummy'), '{%s}cxnSp' % NSMAP['p'])

    nvCxnSpPr = etree.SubElement(sp, '{%s}nvCxnSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvCxnSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(sp_id))
    cNvPr.set('name', name)
    etree.SubElement(nvCxnSpPr, '{%s}cNvCxnSpPr' % NSMAP['p'])
    etree.SubElement(nvCxnSpPr, '{%s}nvPr' % NSMAP['p'])

    spPr = etree.SubElement(sp, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(x)); off.set('y', str(y))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(cx)); ext.set('cy', str(cy))
    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', 'line')
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])
    ln = etree.SubElement(spPr, '{%s}ln' % NSMAP['a'])
    ln.set('w', str(line_w))
    sfill = etree.SubElement(ln, '{%s}solidFill' % NSMAP['a'])
    srgb = etree.SubElement(sfill, '{%s}srgbClr' % NSMAP['a'])
    srgb.set('val', color_hex)

    return sp


def make_oval_sp(sp_id, name, x, y, cx, cy, fill_hex='0078D4', text='',
                 font_size=1200, text_color='FFFFFF'):
    """楕円図形"""
    sp = etree.SubElement(etree.Element('dummy'), '{%s}sp' % NSMAP['p'])

    nvSpPr = etree.SubElement(sp, '{%s}nvSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(sp_id)); cNvPr.set('name', name)
    etree.SubElement(nvSpPr, '{%s}cNvSpPr' % NSMAP['p'])
    etree.SubElement(nvSpPr, '{%s}nvPr' % NSMAP['p'])

    spPr = etree.SubElement(sp, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(x)); off.set('y', str(y))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(cx)); ext.set('cy', str(cy))
    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', 'ellipse')
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])
    solidFill = etree.SubElement(spPr, '{%s}solidFill' % NSMAP['a'])
    srgb = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
    srgb.set('val', fill_hex)
    ln = etree.SubElement(spPr, '{%s}ln' % NSMAP['a'])
    etree.SubElement(ln, '{%s}noFill' % NSMAP['a'])

    if text:
        txBody = etree.SubElement(sp, '{%s}txBody' % NSMAP['p'])
        bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % NSMAP['a'])
        bodyPr.set('anchor', 'ctr')
        etree.SubElement(txBody, '{%s}lstStyle' % NSMAP['a'])
        p_el = etree.SubElement(txBody, '{%s}p' % NSMAP['a'])
        pPr = etree.SubElement(p_el, '{%s}pPr' % NSMAP['a'])
        pPr.set('algn', 'ctr')
        r_el = etree.SubElement(p_el, '{%s}r' % NSMAP['a'])
        rPr = etree.SubElement(r_el, '{%s}rPr' % NSMAP['a'])
        rPr.set('lang', 'ja-JP'); rPr.set('sz', str(font_size)); rPr.set('b', '1')
        sf = etree.SubElement(rPr, '{%s}solidFill' % NSMAP['a'])
        sc = etree.SubElement(sf, '{%s}srgbClr' % NSMAP['a'])
        sc.set('val', text_color)
        latin = etree.SubElement(rPr, '{%s}latin' % NSMAP['a'])
        latin.set('typeface', 'Yu Gothic UI')
        ea = etree.SubElement(rPr, '{%s}ea' % NSMAP['a'])
        ea.set('typeface', 'Yu Gothic UI')
        t_el = etree.SubElement(r_el, '{%s}t' % NSMAP['a'])
        t_el.text = text

    return sp


def make_bg_flower_pic():
    """テンプレート既存の花ぼかし背景画像 (Layout 3/4 と同じ) を <p:pic> として生成。
    rId2=image5.png, rId3=hdphoto1.wdp を参照する。"""
    NS_A = NSMAP['a']
    NS_P = NSMAP['p']
    NS_R = NSMAP['r']
    NS_A14 = 'http://schemas.microsoft.com/office/drawing/2010/main'

    pic = etree.SubElement(etree.Element('dummy'), '{%s}pic' % NS_P)

    # nvPicPr
    nvPicPr = etree.SubElement(pic, '{%s}nvPicPr' % NS_P)
    cNvPr = etree.SubElement(nvPicPr, '{%s}cNvPr' % NS_P)
    cNvPr.set('id', '2')
    cNvPr.set('name', 'Background Picture')
    cNvPicPr = etree.SubElement(nvPicPr, '{%s}cNvPicPr' % NS_P)
    picLocks = etree.SubElement(cNvPicPr, '{%s}picLocks' % NS_A)
    picLocks.set('noChangeAspect', '1')
    etree.SubElement(nvPicPr, '{%s}nvPr' % NS_P)

    # blipFill
    blipFill = etree.SubElement(pic, '{%s}blipFill' % NS_P)
    blipFill.set('rotWithShape', '1')
    blip = etree.SubElement(blipFill, '{%s}blip' % NS_A)
    blip.set('{%s}embed' % NS_R, 'rId2')
    extLst = etree.SubElement(blip, '{%s}extLst' % NS_A)
    # artisticBlur extension
    ext1 = etree.SubElement(extLst, '{%s}ext' % NS_A)
    ext1.set('uri', '{BEBA8EAE-BF5A-486C-A8C5-ECC9F3942E4B}')
    imgProps = etree.SubElement(ext1, '{%s}imgProps' % NS_A14)
    imgLayer = etree.SubElement(imgProps, '{%s}imgLayer' % NS_A14)
    imgLayer.set('{%s}embed' % NS_R, 'rId3')
    imgEffect = etree.SubElement(imgLayer, '{%s}imgEffect' % NS_A14)
    blur = etree.SubElement(imgEffect, '{%s}artisticBlur' % NS_A14)
    blur.set('radius', '75')
    # useLocalDpi extension
    ext2 = etree.SubElement(extLst, '{%s}ext' % NS_A)
    ext2.set('uri', '{28A0092B-C50C-407E-A947-70E740481C1C}')
    dpi = etree.SubElement(ext2, '{%s}useLocalDpi' % NS_A14)
    dpi.set('val', '0')
    # srcRect & stretch
    srcRect = etree.SubElement(blipFill, '{%s}srcRect' % NS_A)
    srcRect.set('t', '2407')
    etree.SubElement(blipFill, '{%s}stretch' % NS_A)

    # spPr
    spPr = etree.SubElement(pic, '{%s}spPr' % NS_P)
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NS_A)
    off = etree.SubElement(xfrm, '{%s}off' % NS_A)
    off.set('x', '0'); off.set('y', '0')
    ext = etree.SubElement(xfrm, '{%s}ext' % NS_A)
    ext.set('cx', str(SLIDE_W)); ext.set('cy', str(SLIDE_H))
    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NS_A)
    prstGeom.set('prst', 'rect')
    etree.SubElement(prstGeom, '{%s}avLst' % NS_A)

    return pic


def build_layout_xml(name, shapes):
    """スライドレイアウト XML ドキュメントを構築"""
    root = etree.Element('{%s}sldLayout' % NSMAP['p'], nsmap=NSMAP)
    root.set('preserve', '1')

    cSld = etree.SubElement(root, '{%s}cSld' % NSMAP['p'])
    cSld.set('name', name)

    spTree = etree.SubElement(cSld, '{%s}spTree' % NSMAP['p'])
    nvGrpSpPr = etree.SubElement(spTree, '{%s}nvGrpSpPr' % NSMAP['p'])
    cNvPr_grp = etree.SubElement(nvGrpSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr_grp.set('id', '1'); cNvPr_grp.set('name', '')
    etree.SubElement(nvGrpSpPr, '{%s}cNvGrpSpPr' % NSMAP['p'])
    etree.SubElement(nvGrpSpPr, '{%s}nvPr' % NSMAP['p'])
    grpSpPr = etree.SubElement(spTree, '{%s}grpSpPr' % NSMAP['p'])
    xfrm = etree.SubElement(grpSpPr, '{%s}xfrm' % NSMAP['a'])
    for tag in ['off', 'ext', 'chOff', 'chExt']:
        el = etree.SubElement(xfrm, '{%s}%s' % (NSMAP['a'], tag))
        el.set('x' if 'Off' in tag or tag == 'off' else 'cx', '0')
        el.set('y' if 'Off' in tag or tag == 'off' else 'cy', '0')

    # ★ テンプレートの花ぼかし背景画像を最初のシェイプとして追加
    bg_pic = make_bg_flower_pic()
    spTree.append(bg_pic)

    for shape in shapes:
        spTree.append(shape)

    # clrMapOvr (既存レイアウトと同じ)
    clrMapOvr = etree.SubElement(root, '{%s}clrMapOvr' % NSMAP['p'])
    etree.SubElement(clrMapOvr, '{%s}masterClrMapping' % NSMAP['a'])

    # トランジション (既存レイアウトと同じフェード)
    transition = etree.SubElement(root, '{%s}transition' % NSMAP['p'])
    etree.SubElement(transition, '{%s}fade' % NSMAP['p'])

    return root


def build_layout_rels_xml():
    """レイアウト用の .rels ファイル
    rId1: slideMaster1 への参照
    rId2: image5.png (花背景画像)
    rId3: hdphoto1.wdp (artisticBlur 用 HD Photo)
    """
    NS_IMAGE_TYPE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
    NS_HDPHOTO_TYPE = 'http://schemas.microsoft.com/office/2007/relationships/hdphoto'

    root = etree.Element('Relationships', xmlns=NS_REL)
    rel1 = etree.SubElement(root, 'Relationship')
    rel1.set('Id', 'rId1')
    rel1.set('Type', NS_MASTER_TYPE)
    rel1.set('Target', '../slideMasters/slideMaster1.xml')
    rel2 = etree.SubElement(root, 'Relationship')
    rel2.set('Id', 'rId2')
    rel2.set('Type', NS_IMAGE_TYPE)
    rel2.set('Target', '../media/image5.png')
    rel3 = etree.SubElement(root, 'Relationship')
    rel3.set('Id', 'rId3')
    rel3.set('Type', NS_HDPHOTO_TYPE)
    rel3.set('Target', '../media/hdphoto1.wdp')
    return root


# ───────────────────────────────────────────────
# レイアウトパターン定義
# ───────────────────────────────────────────────
def define_layouts():
    """全レイアウトパターンを定義して返す。各要素は (name, shapes_list)。"""
    layouts = []
    sid = 100  # shape id カウンタ

    def next_id():
        nonlocal sid
        sid += 1
        return sid

    # ── 色定数 (テンプレートのテーマカラーに準拠) ──
    # テーマ: dk1=595959, lt1=FFFFFF, lt2=F2F2F2
    # accent1=F4364C, accent2=C03BC4, accent3=0078D4, accent4=FFC000
    # accent5=127A93, accent6=49C5B1
    # 既存レイアウト: 背景=ECF0F8, グラデーション=DAE4F6→D2DEF4
    C_BLUE = '0078D4'       # accent3
    C_DARK = '595959'       # dk1 (テーマのメインテキスト色)
    C_BODY = '595959'       # dk1
    C_WHITE = 'FFFFFF'
    C_LIGHT = 'ECF0F8'      # 既存Layout5の背景色
    C_TEAL = '127A93'       # accent5
    C_ACCENT = '0078D4'     # accent3
    C_PURPLE = 'C03BC4'     # accent2
    C_LIGHT_BLUE = 'DAE4F6' # テンプレートのグラデーション色
    C_LIGHT_PURPLE = 'F0E0F5'  # accent2の淡い版
    C_BORDER = 'C0C8D8'     # テンプレート風のソフトボーダー
    C_SECTION_BG = 'ECF0F8'  # Layout5と同じ背景 (ダークではなく)
    C_GREEN = '49C5B1'      # accent6
    C_GOLD = 'FFC000'       # accent4
    C_RED = 'F4364C'         # accent1
    C_GRAD_TOP = 'DAE4F6'   # グラデーション上部 (既存Layout1/2から)
    C_GRAD_BOT = 'D2DEF4'   # グラデーション下部
    C_SUBTITLE = '8090A0'   # サブタイトル用（テンプレート風の淡いグレーブルー）

    # ─── #2 セクション開始スライド ───
    sid = 200
    shapes = [
        make_text_sp(next_id(), 'section_label', emu(1.5), emu(1.5), emu(10), emu(0.6),
                     '第○章 セクションタイトル', font_size=1200, color_hex=C_BLUE,
                     font_name='Yu Gothic UI'),
        make_text_sp(next_id(), 'section_title', emu(1.5), emu(2.3), emu(10), emu(1.5),
                     '新しい章の始まりを印象づける', font_size=3600, bold=True,
                     color_hex=C_DARK, font_name='Yu Gothic UI'),
        make_text_sp(next_id(), 'section_desc', emu(1.5), emu(4.2), emu(8), emu(1.0),
                     'セクションの概要説明がここに入ります。', font_size=1600,
                     color_hex=C_BODY, font_name='Yu Gothic UI'),
    ]
    layouts.append(('セクション開始スライド', shapes))

    # ─── #3 セクション終了・まとめ ───
    sid = 300
    shapes = [
        make_text_sp(next_id(), 'title', emu(1.5), emu(0.5), emu(10), emu(0.8),
                     'セクション終了・まとめ', font_size=2800, bold=True,
                     color_hex=C_DARK, font_name='Yu Gothic UI'),
        make_text_sp(next_id(), 'subtitle', emu(1.5), emu(1.3), emu(10), emu(0.5),
                     '章の要点を整理して次へつなげる', font_size=1400,
                     color_hex=C_BODY, font_name='Yu Gothic UI'),
        make_rect_sp(next_id(), 'point1_bg', emu(1.5), emu(2.2), emu(9.5), emu(1.2),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'point1', emu(1.8), emu(2.35), emu(9), emu(1.0),
                     '✓ まとめポイント1がここに入ります', font_size=1400,
                     color_hex=C_BODY, font_name='Yu Gothic UI', anchor='ctr'),
        make_rect_sp(next_id(), 'point2_bg', emu(1.5), emu(3.6), emu(9.5), emu(1.2),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'point2', emu(1.8), emu(3.75), emu(9), emu(1.0),
                     '✓ まとめポイント2がここに入ります', font_size=1400,
                     color_hex=C_BODY, font_name='Yu Gothic UI', anchor='ctr'),
        make_rect_sp(next_id(), 'point3_bg', emu(1.5), emu(5.0), emu(9.5), emu(1.2),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'point3', emu(1.8), emu(5.15), emu(9), emu(1.0),
                     '✓ まとめポイント3がここに入ります', font_size=1400,
                     color_hex=C_BODY, font_name='Yu Gothic UI', anchor='ctr'),
    ]
    layouts.append(('セクション終了・まとめ', shapes))

    # ─── #6 2カラム比較 (Before/After) ───
    sid = 600
    col_w = emu(4.8)
    gap = emu(0.4)
    col1_x = (SLIDE_W - col_w * 2 - gap) // 2
    col2_x = col1_x + col_w + gap
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '2カラム比較（Before/After）', font_size=2400, bold=True,
                     color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '変化を左右で対比させるパターン', font_size=1200, color_hex=C_BODY),
        make_text_sp(next_id(), 'label_before', col1_x, emu(1.6), col_w, emu(0.5),
                     'Before', font_size=1800, bold=True, color_hex=C_RED,
                     alignment='ctr'),
        make_rect_sp(next_id(), 'col1_bg', col1_x, emu(2.2), col_w, emu(4.5),
                     fill_hex=C_WHITE, line_hex=C_RED, line_w=19050, rounded=True),
        make_text_sp(next_id(), 'col1_text', col1_x + emu(0.3), emu(2.5), col_w - emu(0.6), emu(3.8),
                     '• 改善前の状況をここに記述\n• 課題や問題点を列挙', font_size=1400,
                     color_hex=C_BODY),
        make_text_sp(next_id(), 'label_after', col2_x, emu(1.6), col_w, emu(0.5),
                     'After', font_size=1800, bold=True, color_hex=C_BLUE,
                     alignment='ctr'),
        make_rect_sp(next_id(), 'col2_bg', col2_x, emu(2.2), col_w, emu(4.5),
                     fill_hex=C_WHITE, line_hex=C_BLUE, line_w=19050, rounded=True),
        make_text_sp(next_id(), 'col2_text', col2_x + emu(0.3), emu(2.5), col_w - emu(0.6), emu(3.8),
                     '• 改善後の状況をここに記述\n• 効果やメリットを列挙', font_size=1400,
                     color_hex=C_BODY),
    ]
    layouts.append(('2カラム比較（Before/After）', shapes))

    # ─── #7 2カラム (テキスト+画像) ───
    sid = 700
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '2カラム（テキスト+画像）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     'テキストと画像を横並びに配置', font_size=1200, color_hex=C_BODY),
        make_text_sp(next_id(), 'text_label', MARGIN_L, emu(1.6), emu(5), emu(0.4),
                     'テキストエリア', font_size=1400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'text_area', MARGIN_L, emu(2.1), emu(5), emu(4.5),
                     '説明文がここに入ります。\n\n• ポイント1\n• ポイント2\n• ポイント3',
                     font_size=1400, color_hex=C_BODY),
        make_img_placeholder(next_id(), 'image', MARGIN_L + emu(5.5), emu(1.6), emu(5.4), emu(5.0)),
    ]
    layouts.append(('2カラム（テキスト+画像）', shapes))

    # ─── #7b 2カラム (画像+テキスト) ───
    sid = 750
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '2カラム（画像+テキスト）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '画像とテキストを横並びに配置（逆パターン）', font_size=1200, color_hex=C_BODY),
        make_img_placeholder(next_id(), 'image', MARGIN_L, emu(1.6), emu(5.4), emu(5.0)),
        make_text_sp(next_id(), 'text_label', MARGIN_L + emu(5.9), emu(1.6), emu(5), emu(0.4),
                     'テキストエリア', font_size=1400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'text_area', MARGIN_L + emu(5.9), emu(2.1), emu(5), emu(4.5),
                     '説明文がここに入ります。\n\n• ポイント1\n• ポイント2\n• ポイント3',
                     font_size=1400, color_hex=C_BODY),
    ]
    layouts.append(('2カラム（画像+テキスト）', shapes))

    # ─── #8 3カラム (画像+テキスト) ───
    sid = 800
    c3_w = emu(3.2)
    c3_gap = emu(0.45)
    c3_start = (SLIDE_W - c3_w * 3 - c3_gap * 2) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '3カラム（画像+テキスト）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '画像カードを横に3つ並べる', font_size=1200, color_hex=C_BODY),
    ]
    for i in range(3):
        cx = c3_start + (c3_w + c3_gap) * i
        labels = ['データ分析', 'チームワーク', 'イノベーション']
        shapes.append(make_img_placeholder(next_id(), 'img%d' % i, cx, emu(1.6), c3_w, emu(2.8)))
        shapes.append(make_text_sp(next_id(), 'label%d' % i, cx, emu(4.5), c3_w, emu(0.5),
                                   labels[i], font_size=1400, bold=True, color_hex=C_DARK,
                                   alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'desc%d' % i, cx, emu(5.0), c3_w, emu(1.5),
                                   '説明文がここに入ります。', font_size=1200,
                                   color_hex=C_BODY, alignment='ctr'))
    layouts.append(('3カラム（画像+テキスト）', shapes))

    # ─── #9 3カラム (アクセントカラー付き) ───
    sid = 900
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '3カラム（アクセントカラー付き）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '色で3つの項目を区別する', font_size=1200, color_hex=C_BODY),
    ]
    colors = [C_BLUE, C_TEAL, C_PURPLE]
    labels = ['項目1', '項目2', '項目3']
    for i in range(3):
        cx = c3_start + (c3_w + c3_gap) * i
        shapes.append(make_rect_sp(next_id(), 'header%d' % i, cx, emu(1.6), c3_w, emu(0.7),
                                   fill_hex=colors[i]))
        shapes.append(make_text_sp(next_id(), 'label%d' % i, cx, emu(1.65), c3_w, emu(0.6),
                                   labels[i], font_size=1600, bold=True, color_hex=C_WHITE,
                                   alignment='ctr', anchor='ctr'))
        shapes.append(make_rect_sp(next_id(), 'body%d' % i, cx, emu(2.3), c3_w, emu(4.0),
                                   fill_hex=C_WHITE, line_hex=colors[i], line_w=12700))
        shapes.append(make_text_sp(next_id(), 'desc%d' % i, cx + emu(0.2), emu(2.5),
                                   c3_w - emu(0.4), emu(3.6),
                                   '説明文がここに入ります。', font_size=1300,
                                   color_hex=C_BODY))
    layouts.append(('3カラム（アクセントカラー付き）', shapes))

    # ─── #10 4カラムレイアウト ───
    sid = 1000
    c4_w = emu(2.4)
    c4_gap = emu(0.3)
    c4_start = (SLIDE_W - c4_w * 4 - c4_gap * 3) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '4カラムレイアウト', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '4つのフェーズや選択肢を並べる', font_size=1200, color_hex=C_BODY),
    ]
    phase_labels = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
    for i in range(4):
        cx = c4_start + (c4_w + c4_gap) * i
        shapes.append(make_rect_sp(next_id(), 'card%d' % i, cx, emu(1.6), c4_w, emu(5.0),
                                   fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True))
        shapes.append(make_text_sp(next_id(), 'phase%d' % i, cx, emu(1.8), c4_w, emu(0.5),
                                   phase_labels[i], font_size=1400, bold=True,
                                   color_hex=C_BLUE, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'desc%d' % i, cx + emu(0.15), emu(2.5),
                                   c4_w - emu(0.3), emu(3.8),
                                   '説明文がここに入ります。', font_size=1100,
                                   color_hex=C_BODY, alignment='ctr'))
    layouts.append(('4カラムレイアウト', shapes))

    # ─── #11 5カラム (成熟度レベル) ───
    sid = 1100
    c5_w = emu(1.9)
    c5_gap = emu(0.2)
    c5_start = (SLIDE_W - c5_w * 5 - c5_gap * 4) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '5カラム（成熟度レベル）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '段階的な進化をグラデーションで表現', font_size=1200, color_hex=C_BODY),
    ]
    level_colors = ['B0D4F1', '7AB8E0', '4A9CD4', '2080C0', '0060A0']
    for i in range(5):
        cx = c5_start + (c5_w + c5_gap) * i
        shapes.append(make_rect_sp(next_id(), 'level%d' % i, cx, emu(1.8), c5_w, emu(4.5),
                                   fill_hex=level_colors[i], rounded=True))
        shapes.append(make_text_sp(next_id(), 'label%d' % i, cx, emu(2.0), c5_w, emu(0.5),
                                   'Level %d' % (i + 1), font_size=1400, bold=True,
                                   color_hex=C_WHITE if i >= 2 else C_DARK, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'desc%d' % i, cx + emu(0.1), emu(2.7),
                                   c5_w - emu(0.2), emu(3.3),
                                   '説明', font_size=1000,
                                   color_hex=C_WHITE if i >= 2 else C_DARK, alignment='ctr'))
    layouts.append(('5カラム（成熟度レベル）', shapes))

    # ─── #12 2x2グリッド (画像+テキスト) ───
    sid = 1200
    g_w = emu(4.8)
    g_h = emu(2.5)
    g_gap = emu(0.4)
    g_start_x = (SLIDE_W - g_w * 2 - g_gap) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '2×2グリッド（画像+テキスト）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '4つの要素を2行2列で整理', font_size=1200, color_hex=C_BODY),
    ]
    grid_labels = ['データ分析', 'チームワーク', 'イノベーション', '成果報告']
    for r in range(2):
        for c in range(2):
            idx = r * 2 + c
            gx = g_start_x + (g_w + g_gap) * c
            gy = emu(1.6) + (g_h + g_gap) * r
            shapes.append(make_rect_sp(next_id(), 'card%d' % idx, gx, gy, g_w, g_h,
                                       fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True))
            shapes.append(make_img_placeholder(next_id(), 'img%d' % idx,
                                               gx + emu(0.2), gy + emu(0.2),
                                               emu(1.5), emu(1.5)))
            shapes.append(make_text_sp(next_id(), 'label%d' % idx,
                                       gx + emu(2.0), gy + emu(0.3),
                                       emu(2.5), emu(0.5),
                                       grid_labels[idx], font_size=1400, bold=True,
                                       color_hex=C_DARK))
            shapes.append(make_text_sp(next_id(), 'desc%d' % idx,
                                       gx + emu(2.0), gy + emu(0.9),
                                       emu(2.5), emu(1.3),
                                       '説明文がここに入ります。', font_size=1200,
                                       color_hex=C_BODY))
    layouts.append(('2×2グリッド（画像+テキスト）', shapes))

    # ─── #13 2x3グリッドレイアウト ───
    sid = 1300
    g6_w = emu(3.2)
    g6_h = emu(2.3)
    g6_gap_x = emu(0.35)
    g6_gap_y = emu(0.3)
    g6_start_x = (SLIDE_W - g6_w * 3 - g6_gap_x * 2) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '2×3グリッドレイアウト', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '6つの要素を2行3列で整理', font_size=1200, color_hex=C_BODY),
    ]
    for r in range(2):
        for c in range(3):
            idx = r * 3 + c
            gx = g6_start_x + (g6_w + g6_gap_x) * c
            gy = emu(1.5) + (g6_h + g6_gap_y) * r
            shapes.append(make_rect_sp(next_id(), 'cell%d' % idx, gx, gy, g6_w, g6_h,
                                       fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True))
            shapes.append(make_text_sp(next_id(), 'label%d' % idx,
                                       gx + emu(0.2), gy + emu(0.2), g6_w - emu(0.4), emu(0.5),
                                       '項目%d' % (idx + 1), font_size=1400, bold=True,
                                       color_hex=C_DARK))
            shapes.append(make_text_sp(next_id(), 'desc%d' % idx,
                                       gx + emu(0.2), gy + emu(0.8), g6_w - emu(0.4), emu(1.2),
                                       '説明文がここに入ります。', font_size=1100,
                                       color_hex=C_BODY))
    layouts.append(('2×3グリッドレイアウト', shapes))

    # ─── #14 縦3つステップ ───
    sid = 1400
    step_w = emu(9.5)
    step_x = (SLIDE_W - step_w) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '縦3つステップ', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '番号付きで順序を明示する', font_size=1200, color_hex=C_BODY),
    ]
    for i in range(3):
        sy = emu(1.7) + emu(1.7) * i
        shapes.append(make_oval_sp(next_id(), 'num%d' % i,
                                   step_x, sy + emu(0.15), emu(0.5), emu(0.5),
                                   fill_hex=C_BLUE, text=str(i + 1),
                                   font_size=1400, text_color=C_WHITE))
        shapes.append(make_text_sp(next_id(), 'step_title%d' % i,
                                   step_x + emu(0.8), sy, emu(3.0), emu(0.5),
                                   'ステップ%d' % (i + 1), font_size=1600, bold=True,
                                   color_hex=C_DARK))
        shapes.append(make_text_sp(next_id(), 'step_desc%d' % i,
                                   step_x + emu(0.8), sy + emu(0.5), emu(8.0), emu(1.0),
                                   'このステップの詳細説明がここに入ります。',
                                   font_size=1300, color_hex=C_BODY))
        if i < 2:
            shapes.append(make_line_sp(next_id(), 'connector%d' % i,
                                       step_x + emu(0.25), sy + emu(0.7),
                                       0, emu(0.9), color_hex='B0D4F1', line_w=19050))
    layouts.append(('縦3つステップ', shapes))

    # ─── #15 番号付きステップ (横型) ───
    sid = 1500
    hs_w = emu(2.2)
    hs_gap = emu(0.5)
    hs_count = 4
    hs_start = (SLIDE_W - hs_w * hs_count - hs_gap * (hs_count - 1)) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '番号付きステップ（横型）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '矢印でプロセスの流れを示す', font_size=1200, color_hex=C_BODY),
    ]
    for i in range(hs_count):
        hx = hs_start + (hs_w + hs_gap) * i
        shapes.append(make_oval_sp(next_id(), 'num%d' % i,
                                   hx + emu(0.85), emu(1.8), emu(0.5), emu(0.5),
                                   fill_hex=C_BLUE, text=str(i + 1),
                                   font_size=1400, text_color=C_WHITE))
        shapes.append(make_text_sp(next_id(), 'label%d' % i, hx, emu(2.5), hs_w, emu(0.5),
                                   'ステップ%d' % (i + 1), font_size=1400, bold=True,
                                   color_hex=C_DARK, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'desc%d' % i, hx, emu(3.1), hs_w, emu(3.0),
                                   '説明文', font_size=1100, color_hex=C_BODY, alignment='ctr'))
        if i < hs_count - 1:
            shapes.append(make_text_sp(next_id(), 'arrow%d' % i,
                                       hx + hs_w, emu(2.3), emu(0.5), emu(0.5),
                                       '→', font_size=2000, bold=True, color_hex=C_BLUE,
                                       alignment='ctr'))
    layouts.append(('番号付きステップ（横型）', shapes))

    # ─── #16 タイムラインレイアウト ───
    sid = 1600
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'タイムラインレイアウト', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '時系列で出来事を並べる', font_size=1200, color_hex=C_BODY),
        make_line_sp(next_id(), 'timeline_bar', emu(1.8), emu(3.4), 0, emu(3.5),
                     color_hex=C_BLUE, line_w=25400),
    ]
    events = ['イベント1', 'イベント2', 'イベント3']
    for i, ev in enumerate(events):
        ey = emu(1.8) + emu(1.6) * i
        shapes.append(make_oval_sp(next_id(), 'dot%d' % i,
                                   emu(1.6), ey + emu(0.1), emu(0.4), emu(0.4),
                                   fill_hex=C_BLUE))
        shapes.append(make_rect_sp(next_id(), 'event_bg%d' % i,
                                   emu(2.5), ey, emu(8.5), emu(1.2),
                                   fill_hex=C_LIGHT_BLUE, line_hex=C_BLUE, line_w=12700,
                                   rounded=True))
        shapes.append(make_text_sp(next_id(), 'event%d' % i,
                                   emu(2.8), ey + emu(0.1), emu(8), emu(0.5),
                                   ev, font_size=1400, bold=True, color_hex=C_DARK))
        shapes.append(make_text_sp(next_id(), 'event_desc%d' % i,
                                   emu(2.8), ey + emu(0.6), emu(8), emu(0.5),
                                   '詳細説明がここに入ります。', font_size=1200,
                                   color_hex=C_BODY))
    layouts.append(('タイムラインレイアウト', shapes))

    # ─── #17 アイコン付きリスト ───
    sid = 1700
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'アイコン付きリスト', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '絵文字やアイコンで視覚的に区別', font_size=1200, color_hex=C_BODY),
    ]
    icon_items = [('📊', '項目タイトル1'), ('💡', '項目タイトル2'), ('🎯', '項目タイトル3')]
    for i, (icon, label) in enumerate(icon_items):
        iy = emu(1.7) + emu(1.6) * i
        shapes.append(make_text_sp(next_id(), 'icon%d' % i,
                                   emu(2.0), iy, emu(0.6), emu(0.6),
                                   icon, font_size=2400, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'item_title%d' % i,
                                   emu(3.0), iy, emu(7.5), emu(0.5),
                                   label, font_size=1600, bold=True, color_hex=C_DARK))
        shapes.append(make_text_sp(next_id(), 'item_desc%d' % i,
                                   emu(3.0), iy + emu(0.5), emu(7.5), emu(0.8),
                                   '項目の説明文がここに入ります。', font_size=1300,
                                   color_hex=C_BODY))
    layouts.append(('アイコン付きリスト', shapes))

    # ─── #18 基本パネル (画像ヘッダー付き) ───
    sid = 1800
    p_w = emu(4.8)
    p_gap = emu(0.6)
    p_start = (SLIDE_W - p_w * 2 - p_gap) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '基本パネル（画像ヘッダー付き）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '画像とテキストを組み合わせたカード', font_size=1200, color_hex=C_BODY),
    ]
    for i in range(2):
        px = p_start + (p_w + p_gap) * i
        shapes.append(make_rect_sp(next_id(), 'card%d' % i, px, emu(1.6), p_w, emu(5.0),
                                   fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True))
        shapes.append(make_img_placeholder(next_id(), 'img%d' % i,
                                           px + emu(0.3), emu(1.9), p_w - emu(0.6), emu(2.3)))
        shapes.append(make_text_sp(next_id(), 'panel_title%d' % i,
                                   px + emu(0.3), emu(4.4), p_w - emu(0.6), emu(0.5),
                                   'パネルタイトル%d' % (i + 1), font_size=1400, bold=True,
                                   color_hex=C_DARK))
        shapes.append(make_text_sp(next_id(), 'panel_desc%d' % i,
                                   px + emu(0.3), emu(5.0), p_w - emu(0.6), emu(1.3),
                                   '説明文がここに入ります。', font_size=1200,
                                   color_hex=C_BODY))
    layouts.append(('基本パネル（画像ヘッダー付き）', shapes))

    # ─── #19 強調パネル (左ボーダー付き) ───
    sid = 1900
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '強調パネル（左ボーダー付き）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '左端のラインで重要度を示す', font_size=1200, color_hex=C_BODY),
    ]
    panel_labels = ['パネルタイトル1', 'パネルタイトル2']
    p19_w = emu(4.8)
    p19_gap = emu(0.6)
    p19_start = (SLIDE_W - p19_w * 2 - p19_gap) // 2
    border_colors = [C_BLUE, C_TEAL]
    for i in range(2):
        px = p19_start + (p19_w + p19_gap) * i
        shapes.append(make_rect_sp(next_id(), 'border%d' % i,
                                   px, emu(1.6), emu(0.08), emu(4.8),
                                   fill_hex=border_colors[i]))
        shapes.append(make_rect_sp(next_id(), 'panel%d' % i,
                                   px + emu(0.08), emu(1.6), p19_w - emu(0.08), emu(4.8),
                                   fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700))
        shapes.append(make_text_sp(next_id(), 'panel_title%d' % i,
                                   px + emu(0.4), emu(1.9), p19_w - emu(0.8), emu(0.5),
                                   panel_labels[i], font_size=1600, bold=True,
                                   color_hex=C_DARK))
        shapes.append(make_text_sp(next_id(), 'panel_desc%d' % i,
                                   px + emu(0.4), emu(2.6), p19_w - emu(0.8), emu(3.5),
                                   '説明文がここに入ります。\n\n• ポイント1\n• ポイント2',
                                   font_size=1300, color_hex=C_BODY))
    layouts.append(('強調パネル（左ボーダー付き）', shapes))

    # ─── #20 ガラス風パネル ───
    sid = 2000
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'ガラス風パネル', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '背景を透かして洗練された印象に', font_size=1200, color_hex=C_SUBTITLE),
        make_rect_sp(next_id(), 'glass', emu(2.0), emu(2.0), emu(9.3), emu(4.5),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700,
                     rounded=True),
        make_text_sp(next_id(), 'glass_title', emu(2.5), emu(2.3), emu(8.3), emu(0.7),
                     'ガラス風パネルタイトル', font_size=2000, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'glass_body', emu(2.5), emu(3.2), emu(8.3), emu(3.0),
                     '説明文がここに入ります。背景は透明で見える、名前はほぼ同じ。',
                     font_size=1400, color_hex=C_BODY),
    ]
    layouts.append(('ガラス風パネル', shapes))

    # ─── #21 グラデーションパネル ───
    sid = 2100
    gp_w = emu(4.8)
    gp_gap = emu(0.6)
    gp_start = (SLIDE_W - gp_w * 2 - gp_gap) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'グラデーションパネル', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '色の変化で目を引くパネル', font_size=1200, color_hex=C_BODY),
        make_rect_sp(next_id(), 'panel1', gp_start, emu(1.6), gp_w, emu(5.0),
                     fill_hex=C_BLUE, rounded=True),
        make_text_sp(next_id(), 'p1_title', gp_start + emu(0.3), emu(2.0),
                     gp_w - emu(0.6), emu(0.6),
                     'アクセントパネル', font_size=1600, bold=True, color_hex=C_WHITE),
        make_text_sp(next_id(), 'p1_desc', gp_start + emu(0.3), emu(2.8),
                     gp_w - emu(0.6), emu(3.5),
                     '説明文がここに入ります。', font_size=1300, color_hex=C_LIGHT),
        make_rect_sp(next_id(), 'panel2', gp_start + gp_w + gp_gap, emu(1.6), gp_w, emu(5.0),
                     fill_hex='E8F4FD', rounded=True),
        make_text_sp(next_id(), 'p2_title', gp_start + gp_w + gp_gap + emu(0.3), emu(2.0),
                     gp_w - emu(0.6), emu(0.6),
                     '明るいグラデーション', font_size=1600, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'p2_desc', gp_start + gp_w + gp_gap + emu(0.3), emu(2.8),
                     gp_w - emu(0.6), emu(3.5),
                     '説明文がここに入ります。', font_size=1300, color_hex=C_BODY),
    ]
    layouts.append(('グラデーションパネル', shapes))

    # ─── #22 カード型レイアウト (画像付き) ───
    sid = 2200
    ck_w = emu(2.4)
    ck_gap = emu(0.3)
    ck_count = 4
    ck_start = (SLIDE_W - ck_w * ck_count - ck_gap * (ck_count - 1)) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'カード型レイアウト（画像付き）', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '製品やサービスを紹介するカード', font_size=1200, color_hex=C_BODY),
    ]
    card_labels = ['品質管理', '技術開発', '顧客満足', '競争優位']
    for i in range(ck_count):
        cx = ck_start + (ck_w + ck_gap) * i
        shapes.append(make_rect_sp(next_id(), 'card%d' % i, cx, emu(1.6), ck_w, emu(5.0),
                                   fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True))
        shapes.append(make_img_placeholder(next_id(), 'img%d' % i,
                                           cx + emu(0.2), emu(1.8), ck_w - emu(0.4), emu(2.0)))
        shapes.append(make_text_sp(next_id(), 'label%d' % i, cx, emu(4.0), ck_w, emu(0.5),
                                   card_labels[i], font_size=1200, bold=True,
                                   color_hex=C_DARK, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'desc%d' % i, cx + emu(0.15), emu(4.6),
                                   ck_w - emu(0.3), emu(1.8),
                                   '説明文', font_size=1000, color_hex=C_BODY, alignment='ctr'))
    layouts.append(('カード型レイアウト（画像付き）', shapes))

    # ─── #23 背景画像全画面 ───
    sid = 2300
    shapes = [
        make_text_sp(next_id(), 'title', emu(2.0), emu(2.0), emu(9.3), emu(1.5),
                     'キャッチコピーが\nここに入ります', font_size=3600, bold=True,
                     color_hex=C_DARK, alignment='ctr'),
        make_text_sp(next_id(), 'desc', emu(2.0), emu(4.0), emu(9.3), emu(1.0),
                     'インパクトのある一文をここに', font_size=1600,
                     color_hex=C_BODY, alignment='ctr'),
    ]
    layouts.append(('背景画像全画面', shapes))

    # ─── #24 背景画像右側配置 ───
    sid = 2400
    shapes = [
        make_text_sp(next_id(), 'title', emu(1.0), emu(0.8), emu(5.5), emu(1.0),
                     '背景画像右側配置', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'body', emu(1.0), emu(2.0), emu(5.5), emu(4.5),
                     '説明文がここに入ります。背景は右に画る。\n\n• ポイント1\n• ポイント2',
                     font_size=1400, color_hex=C_BODY),
        make_img_placeholder(next_id(), 'right_img', emu(7.0), emu(0.0), emu(6.3), SLIDE_H),
    ]
    layouts.append(('背景画像右側配置', shapes))

    # ─── #25 引用スライド ───
    sid = 2500
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.6),
                     '引用スライド', font_size=2000, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(0.9), CONTENT_W, emu(0.4),
                     '印象的な言葉を引用する', font_size=1200, color_hex=C_SUBTITLE),
        make_rect_sp(next_id(), 'quote_bg', emu(2.0), emu(2.0), emu(9.3), emu(3.5),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True),
        make_rect_sp(next_id(), 'quote_bar', emu(2.3), emu(2.4), emu(0.06), emu(2.7),
                     fill_hex=C_BLUE),
        make_text_sp(next_id(), 'quote', emu(2.7), emu(2.5), emu(8.3), emu(2.0),
                     '「ここに引用文を入力します。インスピレーションを与える言葉を選びましょう。」',
                     font_size=1800, color_hex=C_DARK, font_name='Yu Gothic UI'),
        make_text_sp(next_id(), 'author', emu(2.7), emu(4.8), emu(8.3), emu(0.5),
                     '― 著者名', font_size=1200, color_hex=C_BLUE,
                     alignment='r'),
    ]
    layouts.append(('引用スライド', shapes))

    # ─── #26 複数画像・分割背景 ───
    sid = 2600
    mi_w = emu(4.8)
    mi_gap = emu(0.5)
    mi_start = (SLIDE_W - mi_w * 2 - mi_gap) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '複数画像・分割背景', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '複数の画像を横並びで見せる', font_size=1200, color_hex=C_BODY),
        make_img_placeholder(next_id(), 'img1', mi_start, emu(1.6), mi_w, emu(5.0)),
        make_img_placeholder(next_id(), 'img2', mi_start + mi_w + mi_gap, emu(1.6), mi_w, emu(5.0)),
        make_text_sp(next_id(), 'caption', emu(1.5), emu(6.8), emu(10.3), emu(0.4),
                     '複数の画像を横並びで配置するパターン', font_size=1000,
                     color_hex=C_BODY, alignment='ctr'),
    ]
    layouts.append(('複数画像・分割背景', shapes))

    # ─── #27 統計強調スライド ───
    sid = 2700
    stat_w = emu(3.2)
    stat_gap = emu(0.6)
    stat_start = (SLIDE_W - stat_w * 3 - stat_gap * 2) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '統計強調スライド', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '大きな数字でインパクトを出す', font_size=1200, color_hex=C_BODY),
    ]
    stats = [('60万人', '利用者数'), ('98%', '満足度'), ('3倍', '生産性向上')]
    for i, (num, label) in enumerate(stats):
        sx = stat_start + (stat_w + stat_gap) * i
        shapes.append(make_rect_sp(next_id(), 'stat_bg%d' % i, sx, emu(1.8), stat_w, emu(4.5),
                                   fill_hex=C_LIGHT_BLUE, rounded=True))
        shapes.append(make_text_sp(next_id(), 'stat_num%d' % i,
                                   sx, emu(2.3), stat_w, emu(1.5),
                                   num, font_size=4000, bold=True, color_hex=C_BLUE,
                                   alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'stat_label%d' % i,
                                   sx, emu(4.0), stat_w, emu(0.6),
                                   label, font_size=1600, color_hex=C_DARK, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'stat_desc%d' % i,
                                   sx + emu(0.2), emu(4.8), stat_w - emu(0.4), emu(1.2),
                                   '補足説明がここに入ります。', font_size=1100,
                                   color_hex=C_BODY, alignment='ctr'))
    layouts.append(('統計強調スライド', shapes))

    # ─── #28 中央配置メッセージ ───
    sid = 2800
    shapes = [
        make_text_sp(next_id(), 'label', emu(2.0), emu(0.8), emu(9.3), emu(0.5),
                     '中央配置メッセージ', font_size=1400, color_hex=C_BODY, alignment='ctr'),
        make_text_sp(next_id(), 'desc', emu(2.0), emu(1.2), emu(9.3), emu(0.4),
                     'シンプルに一言を伝える', font_size=1100, color_hex=C_BODY, alignment='ctr'),
        make_text_sp(next_id(), 'message', emu(1.5), emu(2.5), emu(10.3), emu(2.0),
                     '大きなメッセージが\nここに入ります', font_size=3600, bold=True,
                     color_hex=C_DARK, alignment='ctr', anchor='ctr'),
        make_text_sp(next_id(), 'english', emu(2.0), emu(4.8), emu(9.3), emu(0.5),
                     'English message here', font_size=1400, color_hex=C_BODY, alignment='ctr'),
        make_line_sp(next_id(), 'divider', emu(5.5), emu(5.5), emu(2.3), 0,
                     color_hex=C_BORDER, line_w=12700),
        make_text_sp(next_id(), 'author', emu(2.0), emu(5.8), emu(9.3), emu(0.5),
                     '— 引用元、等', font_size=1200, color_hex=C_BODY, alignment='ctr'),
    ]
    layouts.append(('中央配置メッセージ', shapes))

    # ─── #29 Q&Aスライド ───
    sid = 2900
    shapes = [
        make_text_sp(next_id(), 'qa_label', emu(3.0), emu(1.5), emu(7.3), emu(1.5),
                     'Q&A', font_size=5400, bold=True, color_hex=C_DARK, alignment='ctr'),
        make_text_sp(next_id(), 'qa_desc', emu(3.0), emu(3.5), emu(7.3), emu(1.0),
                     'ご質問をお待ちしています', font_size=1800, color_hex=C_BODY,
                     alignment='ctr'),
    ]
    layouts.append(('Q&Aスライド', shapes))

    # ─── #30 QRコード付き紹介 ───
    sid = 3000
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'QRコード付き紹介', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '書籍やサイトへ誘導する', font_size=1200, color_hex=C_BODY),
        make_rect_sp(next_id(), 'qr_area', emu(2.0), emu(2.0), emu(3.5), emu(3.5),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700),
        make_text_sp(next_id(), 'qr_label', emu(2.0), emu(3.0), emu(3.5), emu(1.0),
                     'QR コード\nをここに配置', font_size=1600, color_hex=C_BODY, alignment='ctr',
                     anchor='ctr'),
        make_text_sp(next_id(), 'url', emu(2.0), emu(5.7), emu(3.5), emu(0.4),
                     'https://example.com', font_size=1000, color_hex=C_BLUE, alignment='ctr'),
        make_text_sp(next_id(), 'info_title', emu(6.5), emu(2.0), emu(5.3), emu(0.6),
                     'リソース名', font_size=1800, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'info_body', emu(6.5), emu(2.8), emu(5.3), emu(3.5),
                     '説明文がここに入ります。\n\nスキャンしてアクセスしてください。',
                     font_size=1400, color_hex=C_BODY),
    ]
    layouts.append(('QRコード付き紹介', shapes))

    # ─── #31 問いかけスライド ───
    sid = 3100
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.5), CONTENT_W, emu(0.6),
                     '問いかけスライド', font_size=2000, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '聴衆への問いを中央配置で投げかける', font_size=1200, color_hex=C_SUBTITLE),
        make_rect_sp(next_id(), 'question_bg', emu(1.5), emu(2.2), emu(10.3), emu(2.5),
                     fill_hex=C_WHITE, line_hex=C_BLUE, line_w=19050, rounded=True),
        make_text_sp(next_id(), 'question', emu(2.0), emu(2.5), emu(9.3), emu(1.8),
                     '「問いかけの文章がここに入ります」',
                     font_size=2400, bold=True, color_hex=C_DARK, alignment='ctr',
                     anchor='ctr'),
        make_text_sp(next_id(), 'note', emu(2.0), emu(5.2), emu(9.3), emu(1.0),
                     '補足説明文がここに入ります。議論したい場合はこのように。',
                     font_size=1300, color_hex=C_BODY, alignment='ctr'),
    ]
    layouts.append(('問いかけスライド', shapes))

    # ─── #32 映画引用スライド ───
    sid = 3200
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.5), CONTENT_W, emu(0.6),
                     '映画引用スライド', font_size=2000, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '映画のセリフを引用して印象づける', font_size=1200, color_hex=C_SUBTITLE),
        make_rect_sp(next_id(), 'quote_frame', emu(2.0), emu(2.0), emu(9.3), emu(2.5),
                     fill_hex=C_WHITE, line_hex=C_BORDER, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'quote', emu(2.5), emu(2.3), emu(8.3), emu(1.5),
                     '「映画のセリフがここに入ります。」',
                     font_size=2000, bold=True, color_hex=C_DARK, alignment='ctr'),
        make_text_sp(next_id(), 'source', emu(2.5), emu(3.8), emu(8.3), emu(0.5),
                     '— 映画タイトル（公開年）', font_size=1200, color_hex=C_BLUE,
                     alignment='r'),
        make_text_sp(next_id(), 'connection', emu(2.0), emu(5.0), emu(9.3), emu(1.0),
                     'この「キーワード」について考えてみましょう。',
                     font_size=1400, color_hex=C_BODY, alignment='ctr'),
    ]
    layouts.append(('映画引用スライド', shapes))

    # ─── #33 インライン画像スライド ───
    sid = 3300
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'インライン画像スライド', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '画像とテキストを並べて解説する', font_size=1200, color_hex=C_BODY),
        make_img_placeholder(next_id(), 'inline_img', MARGIN_L, emu(1.6), emu(3.5), emu(3.5)),
        make_text_sp(next_id(), 'text_area', MARGIN_L + emu(4.0), emu(1.6), emu(6.9), emu(5.0),
                     '説明文がここに入ります。画像とテキストを横並びで配置するパターンです。\n\n'
                     '• HTML/Svgタグで表現\n• Tailored サイズ調整\n• Rawで簡潔に',
                     font_size=1400, color_hex=C_BODY),
    ]
    layouts.append(('インライン画像スライド', shapes))

    # ─── #34 統計比率スライド ───
    sid = 3400
    bar_colors = [C_BLUE, C_TEAL, C_GREEN]
    bar_labels = ['80%', '65%', '74%']
    bar_descs = ['カテゴリA', 'カテゴリB', 'カテゴリC']
    bar_w_base = emu(7.0)
    bars_x = (SLIDE_W - bar_w_base) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '統計比率スライド', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '数値データを視覚的に比較する', font_size=1200, color_hex=C_BODY),
    ]
    ratios = [0.80, 0.65, 0.74]
    for i in range(3):
        by = emu(1.8) + emu(1.4) * i
        bw = int(bar_w_base * ratios[i])
        shapes.append(make_text_sp(next_id(), 'pct%d' % i,
                                   bars_x - emu(1.2), by + emu(0.1), emu(1.0), emu(0.5),
                                   bar_labels[i], font_size=2000, bold=True,
                                   color_hex=bar_colors[i], alignment='r'))
        shapes.append(make_rect_sp(next_id(), 'bar_bg%d' % i,
                                   bars_x, by, bar_w_base, emu(0.7),
                                   fill_hex='E8ECF1', rounded=True))
        shapes.append(make_rect_sp(next_id(), 'bar%d' % i,
                                   bars_x, by, bw, emu(0.7),
                                   fill_hex=bar_colors[i], rounded=True))
        shapes.append(make_text_sp(next_id(), 'bar_label%d' % i,
                                   bars_x, by + emu(0.8), bar_w_base, emu(0.4),
                                   bar_descs[i], font_size=1200, color_hex=C_BODY,
                                   alignment='ctr'))
    shapes.append(make_text_sp(next_id(), 'footnote',
                               emu(2.0), emu(6.2), emu(9.3), emu(0.4),
                               '解説文がここに入ります — 補足説明', font_size=1100,
                               color_hex=C_BODY, alignment='ctr'))
    layouts.append(('統計比率スライド', shapes))

    # ─── #35 テキスト+統計パネル混合 ───
    sid = 3500
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'テキスト+統計パネル混合', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '説明文と数値を組み合わせる', font_size=1200, color_hex=C_BODY),
        make_text_sp(next_id(), 'text_label', MARGIN_L, emu(1.6), emu(5.0), emu(0.4),
                     '説明ラベル', font_size=1400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'text_body', MARGIN_L, emu(2.1), emu(5.0), emu(4.5),
                     '説明文がここに入ります。テキストエリアに詳細を記述します。\n\n'
                     '• ポイント1\n• ポイント2', font_size=1300, color_hex=C_BODY),
    ]
    stat_panels = [('60%', 'ラベルA'), ('1.2M', 'ラベルB')]
    sp_w = emu(2.5)
    sp_gap = emu(0.4)
    sp_start = MARGIN_L + emu(5.5)
    for i, (val, lbl) in enumerate(stat_panels):
        sx = sp_start + (sp_w + sp_gap) * i
        shapes.append(make_rect_sp(next_id(), 'stat_panel%d' % i,
                                   sx, emu(1.6), sp_w, emu(2.8),
                                   fill_hex=C_LIGHT_BLUE, rounded=True))
        shapes.append(make_text_sp(next_id(), 'stat_val%d' % i,
                                   sx, emu(2.0), sp_w, emu(1.0),
                                   val, font_size=2800, bold=True,
                                   color_hex=C_BLUE, alignment='ctr'))
        shapes.append(make_text_sp(next_id(), 'stat_lbl%d' % i,
                                   sx, emu(3.2), sp_w, emu(0.5),
                                   lbl, font_size=1200, color_hex=C_BODY, alignment='ctr'))
    layouts.append(('テキスト+統計パネル混合', shapes))

    # ─── #36 まとめスライド (ガラス風縦並び) ───
    sid = 3600
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'まとめスライド（ガラス風縦並び）', font_size=2400, bold=True,
                     color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     'セクションの要点をガラス風パネルで整理', font_size=1200, color_hex=C_SUBTITLE),
    ]
    summary_items = [
        'まとめポイント1のタイトル',
        'まとめポイント2のタイトル',
        'まとめポイント3のタイトル',
    ]
    panel_w = emu(9.5)
    panel_x = (SLIDE_W - panel_w) // 2
    for i, item in enumerate(summary_items):
        py = emu(1.7) + emu(1.6) * i
        shapes.append(make_rect_sp(next_id(), 'glass%d' % i,
                                   panel_x, py, panel_w, emu(1.3),
                                   fill_hex=C_WHITE, line_hex=C_BORDER,
                                   line_w=12700, rounded=True))
        shapes.append(make_text_sp(next_id(), 'point%d' % i,
                                   panel_x + emu(0.5), py + emu(0.2), panel_w - emu(1.0), emu(0.8),
                                   '✓ %s' % item, font_size=1600, bold=True,
                                   color_hex=C_DARK, anchor='ctr'))
    layouts.append(('まとめスライド（ガラス風縦並び）', shapes))

    # ─── #37 シンプルリスト+補足パネル ───
    sid = 3700
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     'シンプルリスト+補足パネル', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '箇条書きに補足情報を添える', font_size=1200, color_hex=C_BODY),
        make_text_sp(next_id(), 'list', MARGIN_L, emu(1.6), emu(5.5), emu(5.0),
                     '• リスト項目がここに入ります。山括弧で分ける。\n\n'
                     '• 2つ目の項目\n\n• 3つ目の項目\n\n• 複数レベルのインデントにも対応',
                     font_size=1400, color_hex=C_BODY),
        make_rect_sp(next_id(), 'note_panel', MARGIN_L + emu(6.0), emu(1.6),
                     emu(4.9), emu(5.0),
                     fill_hex=C_LIGHT_BLUE, line_hex=C_BLUE, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'note_title', MARGIN_L + emu(6.3), emu(1.9),
                     emu(4.3), emu(0.5),
                     '📌 補足情報', font_size=1400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'note_body', MARGIN_L + emu(6.3), emu(2.5),
                     emu(4.3), emu(3.8),
                     '補足の説明文がここに入ります。\n\nメモや注意点を記載してください。',
                     font_size=1200, color_hex=C_BODY),
    ]
    layouts.append(('シンプルリスト+補足パネル', shapes))

    # ─── #38 対比+結論スライド ───
    sid = 3800
    vs_w = emu(4.5)
    vs_gap = emu(0.5)
    vs_start = (SLIDE_W - vs_w * 2 - vs_gap) // 2
    shapes = [
        make_text_sp(next_id(), 'title', MARGIN_L, emu(0.4), CONTENT_W, emu(0.7),
                     '対比+結論スライド', font_size=2400, bold=True, color_hex=C_DARK),
        make_text_sp(next_id(), 'subtitle', MARGIN_L, emu(1.0), CONTENT_W, emu(0.4),
                     '二項対立から結論を導く', font_size=1200, color_hex=C_BODY),
        # 概念A
        make_rect_sp(next_id(), 'conceptA', vs_start, emu(1.6), vs_w, emu(3.0),
                     fill_hex=C_LIGHT_BLUE, line_hex=C_BLUE, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'labelA', vs_start + emu(0.3), emu(1.8), vs_w - emu(0.6), emu(0.5),
                     '概念A', font_size=1600, bold=True, color_hex=C_BLUE),
        make_text_sp(next_id(), 'descA', vs_start + emu(0.3), emu(2.5), vs_w - emu(0.6), emu(1.8),
                     '概念Aの説明がここに入ります。',
                     font_size=1300, color_hex=C_BODY),
        # 概念B
        make_rect_sp(next_id(), 'conceptB', vs_start + vs_w + vs_gap, emu(1.6), vs_w, emu(3.0),
                     fill_hex=C_LIGHT_PURPLE, line_hex=C_PURPLE, line_w=12700, rounded=True),
        make_text_sp(next_id(), 'labelB', vs_start + vs_w + vs_gap + emu(0.3), emu(1.8),
                     vs_w - emu(0.6), emu(0.5),
                     '概念B', font_size=1600, bold=True, color_hex=C_PURPLE),
        make_text_sp(next_id(), 'descB', vs_start + vs_w + vs_gap + emu(0.3), emu(2.5),
                     vs_w - emu(0.6), emu(1.8),
                     '概念Bの説明がここに入ります。',
                     font_size=1300, color_hex=C_BODY),
        # 結論
        make_rect_sp(next_id(), 'conclusion_bg',
                     (SLIDE_W - emu(9.5)) // 2, emu(5.0), emu(9.5), emu(1.8),
                     fill_hex=C_LIGHT, line_hex=C_BLUE, line_w=19050, rounded=True),
        make_text_sp(next_id(), 'conclusion_label',
                     (SLIDE_W - emu(9.5)) // 2 + emu(0.3), emu(5.1), emu(8.9), emu(0.5),
                     '結論', font_size=1600, bold=True, color_hex=C_BLUE),
        make_text_sp(next_id(), 'conclusion_text',
                     (SLIDE_W - emu(9.5)) // 2 + emu(0.3), emu(5.6), emu(8.9), emu(1.0),
                     '両者を踏まえた結論がここに入ります。',
                     font_size=1400, color_hex=C_BODY),
    ]
    layouts.append(('対比+結論スライド', shapes))

    return layouts


# ───────────────────────────────────────────────
# メイン: テンプレートにレイアウトを追加
# ───────────────────────────────────────────────
def main():
    # バックアップからの復元（常にオリジナルから再構築する）
    backup_path = TEMPLATE_SRC + '.bak'
    if not os.path.exists(backup_path):
        shutil.copy2(TEMPLATE_SRC, backup_path)
        print('バックアップを作成: %s' % backup_path)
    else:
        # バックアップが既にある場合、バックアップから復元して作業する
        shutil.copy2(backup_path, TEMPLATE_SRC)
        print('バックアップから復元: %s' % backup_path)

    # レイアウト定義
    layouts = define_layouts()
    print('%d 個の新レイアウトを追加します...' % len(layouts))

    # テンプレートを読み込み
    with zipfile.ZipFile(TEMPLATE_SRC, 'r') as zin:
        existing_files = {}
        for item in zin.namelist():
            existing_files[item] = zin.read(item)

    # 既存のレイアウト数 (5)
    existing_layout_count = 5
    # 既存の slideMaster rels の最大 rId
    master_rels = etree.fromstring(existing_files['ppt/slideMasters/_rels/slideMaster1.xml.rels'])
    max_rid = 0
    for rel in master_rels:
        rid_num = int(rel.get('Id').replace('rId', ''))
        if rid_num > max_rid:
            max_rid = rid_num

    # Content Types XML
    ct_xml = etree.fromstring(existing_files['[Content_Types].xml'])

    # slideMaster1.xml を解析して sldLayoutIdLst を取得
    NS_P = NSMAP['p']
    NS_R = NSMAP['r']
    master_xml = etree.fromstring(existing_files['ppt/slideMasters/slideMaster1.xml'])
    sld_layout_id_lst = master_xml.find('{%s}sldLayoutIdLst' % NS_P)
    if sld_layout_id_lst is None:
        raise RuntimeError('slideMaster1.xml に sldLayoutIdLst が見つかりません')

    # 既存の最大 layout id を取得
    max_layout_id = 0
    for sld_layout_id in sld_layout_id_lst:
        lid = int(sld_layout_id.get('id', '0'))
        if lid > max_layout_id:
            max_layout_id = lid

    print('  既存の最大 rId: %d, 最大 layoutId: %d' % (max_rid, max_layout_id))

    # 新レイアウトを追加
    for i, (name, shapes) in enumerate(layouts):
        layout_num = existing_layout_count + 1 + i
        layout_filename = 'slideLayout%d.xml' % layout_num
        layout_path = 'ppt/slideLayouts/%s' % layout_filename
        rels_path = 'ppt/slideLayouts/_rels/%s.rels' % layout_filename

        # レイアウト XML 生成
        layout_xml = build_layout_xml(name, shapes)
        layout_bytes = etree.tostring(layout_xml, xml_declaration=True,
                                      encoding='UTF-8', standalone=True)
        existing_files[layout_path] = layout_bytes

        # レイアウト .rels 生成
        rels_xml = build_layout_rels_xml()
        rels_bytes = etree.tostring(rels_xml, xml_declaration=True,
                                    encoding='UTF-8', standalone=True)
        existing_files[rels_path] = rels_bytes

        # slideMaster の .rels に Relationship 追加
        new_rid = max_rid + 1 + i
        rid_str = 'rId%d' % new_rid
        rel_el = etree.SubElement(master_rels, 'Relationship')
        rel_el.set('Id', rid_str)
        rel_el.set('Type', NS_LAYOUT_TYPE)
        rel_el.set('Target', '../slideLayouts/%s' % layout_filename)

        # ★ slideMaster1.xml の <p:sldLayoutIdLst> に <p:sldLayoutId> を追加
        new_layout_id = max_layout_id + 1 + i
        sld_layout_id_el = etree.SubElement(sld_layout_id_lst, '{%s}sldLayoutId' % NS_P)
        sld_layout_id_el.set('id', str(new_layout_id))
        sld_layout_id_el.set('{%s}id' % NS_R, rid_str)

        # Content Types に追加
        override = etree.SubElement(ct_xml, 'Override')
        override.set('PartName', '/%s' % layout_path)
        override.set('ContentType',
                     'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml')

    # 更新した XML を書き戻し
    existing_files['ppt/slideMasters/_rels/slideMaster1.xml.rels'] = \
        etree.tostring(master_rels, xml_declaration=True, encoding='UTF-8', standalone=True)
    existing_files['[Content_Types].xml'] = \
        etree.tostring(ct_xml, xml_declaration=True, encoding='UTF-8', standalone=True)
    existing_files['ppt/slideMasters/slideMaster1.xml'] = \
        etree.tostring(master_xml, xml_declaration=True, encoding='UTF-8', standalone=True)

    # ZIP に書き出し
    with zipfile.ZipFile(TEMPLATE_DST, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in existing_files.items():
            zout.writestr(name, data)

    print('✅ テンプレートを更新しました: %s' % TEMPLATE_DST)
    print('   既存: %d レイアウト + 新規: %d レイアウト = 合計 %d レイアウト' %
          (existing_layout_count, len(layouts), existing_layout_count + len(layouts)))


if __name__ == '__main__':
    main()
