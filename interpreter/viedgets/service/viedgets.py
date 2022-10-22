from interpreter.viedgets.layout.column_viedget import ColumnViedget
from interpreter.viedgets.padding_viedget import PaddingViedget
from interpreter.viedgets.layout.row_viedget import RowViedget
from interpreter.viedgets.layout.stack_viedget import StackViedget
from interpreter.viedgets.scrollable_viedget import ScrollableViedget
from interpreter.viedgets.text_viedget import TextViedget
from interpreter.viedgets.view_viedget import ViewViedget

VIEDGETS = {
    "scrollable": ScrollableViedget,
    "stack": StackViedget,
    "column": ColumnViedget,
    "row": RowViedget,
    "padding": PaddingViedget,
    "text": TextViedget,
    "view": ViewViedget,
}
