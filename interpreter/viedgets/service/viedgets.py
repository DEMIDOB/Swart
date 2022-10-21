from column_viedget import ColumnViedget
from interpreter.viedgets.padding_viedget import PaddingViedget
from interpreter.viedgets.row_viedget import RowViedget
from interpreter.viedgets.stack_viedget import StackViedget
from interpreter.viedgets.text_viedget import TextViedget
from interpreter.viedgets.view_viedget import ViewViedget

VIEDGETS = {
    "stack": StackViedget,
    "column": ColumnViedget,
    "row": RowViedget,
    "padding": PaddingViedget,
    "text": TextViedget,
    "view": ViewViedget,
}
