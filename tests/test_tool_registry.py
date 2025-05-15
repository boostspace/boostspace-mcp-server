from boostspace_mcp.tool_registry import ToolRegistry


def test_fill_path_keeps_extras():
    reg = ToolRegistry(None, None)
    filled, extras = reg._fill_path("/item/{id}", {"id": 7, "q": 1})
    assert filled == "/item/7"
    assert extras == {"q": 1}


def test_fill_path_no_template_vars():
    reg = ToolRegistry(None, None)
    filled, extras = reg._fill_path("/static", {"x": 42})
    assert filled == "/static"
    assert extras == {"x": 42}


def test_generate_tool_id():
    reg = ToolRegistry(None, None)
    tid = reg._generate_tool_id("PATCH", "/custom-module-item/{customModuleItemId}")
    assert tid == "patch_custom-module-item_customModuleItemId"
