from wagtail.core import blocks

from wagtailnhsukfrontend.blocks import (
    ActionLinkBlock,
    CareCardBlock,
    DetailsBlock,
    DoBlock,
    DontBlock,
    ExpanderBlock,
    ExpanderGroupBlock,
    GreyPanelBlock,
    InsetTextBlock,
    ImageBlock,
    PanelBlock,
    PanelListBlock,
    WarningCalloutBlock,
    PromoBlock,
    PromoGroupBlock,
    SummaryListBlock,
)

class PanelBlockWithImage(PanelBlock):
    pass

class CoreBlocks(blocks.StreamBlock):
    action_link = ActionLinkBlock()
    care_card = CareCardBlock()
    details = DetailsBlock()
    do_list = DoBlock()
    dont_list = DontBlock()
    expander = ExpanderBlock()
    expander_group = ExpanderGroupBlock()
    inset_text = InsetTextBlock()
    image = ImageBlock()
    panel = PanelBlock()
    panel_list = PanelListBlock()
    # panel_with_image = PanelBlockWithImage()
    grey_panel = GreyPanelBlock()
    warning_callout = WarningCalloutBlock()
    summary_list = SummaryListBlock()
    promo = PromoBlock()
    promo_group = PromoGroupBlock()


