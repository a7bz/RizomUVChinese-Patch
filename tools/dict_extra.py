"""补充词条：面板标签、按钮提示与长说明文本。

与 gen_dictionary.py 里的表分开维护，避免单文件过大。
键必须与界面上的英文原文完全一致（含空格、标点、制表符）。
"""

from __future__ import annotations

EXTRA: dict[str, str] = {
    # ------------------------------------------------------------ 长说明（完整句）
    "'First Selected' uses the first selected island of the selection sequence as source island and the selection set as destination set.":
        "「首个选中」以选择序列中第一个被选中的岛作为源岛，其余选区作为目标集。",
    "'Selection' uses the selected islands as the source and visible islands as the.":
        "「选择」以选中的岛作为源，以可见岛作为目标。",
    "'Isolate' term that appears in the following means the action to hide others islands and let visible the 'isolated' ones. It is a very convenient feature when dealing with meshes that are segmented in a lot islands. Pressing 'I' hover an island will isolate it, pressing 'Y' will unhide all of them. The 'Auto' isolate feature will isolate islands that have at least one edge selected.":
        "下文中的「孤立」是指隐藏其他岛、只保留被「孤立」的岛。处理被切成大量岛的网格时，这个功能非常方便。悬停在某个岛上按 I 可将其孤立，按 Y 可全部显示。「自动」孤立会孤立至少选中一条边的岛。",
    '- If you are using a multiple tile layout(UDIMs), Spacing and Margin can be set per tile.':
        "· 如果使用多贴图块布局（UDIM），间距与边距可以按贴图块分别设置。",
    '- If you select a group box with unselected content, the box itself moves during a pack, with its content as a non - changeable set.':
        "· 如果你选中了包含未选中内容的组框，排布时组框本身会移动，其内容作为不可变集合随之移动。",
    '- Map Rez is a global parameter and has the same value for all tiles.':
        "· 贴图分辨率是全局参数，所有贴图块取值相同。",
    '- Pack transforms the island and group selection if any.If the selection is empty, all non - hidden islands and groups are packed.':
        "· 排布会变换选中的岛与组；若没有选中任何内容，则排布所有未隐藏的岛与组。",
    '- Should you be on a multiple tile (UDIM) layout, and you select only a few tiles, only the selected tiles and their content are packed.':
        "· 在多贴图块（UDIM）布局下，若只选中少数贴图块，则仅排布这些贴图块及其内容。",
    '- There is a list over how to set margins, Map Rez and spacing on the Rizom - Lab website : https://www.rizom-lab.com/news/uv_mapping_beginner_tips/':
        "· Rizom-Lab 官网有一份关于边距、贴图分辨率与间距设置的说明：https://www.rizom-lab.com/news/uv_mapping_beginner_tips/",
    "0 = Optimize Angles, 1 = Optimize Lengths.": "0 = 优化角度，1 = 优化长度。",
    "1. Pressing the 'TAB' key, then move the gizmo anchor, or":
        "1. 按 TAB 键，然后移动操纵器锚点；或者",
    "2. Pressing the 'SPACE' key, drag the mouse while pressing the left or middle or right button, or":
        "2. 按住 SPACE 键，再按住鼠标左键/中键/右键拖动；或者",
    "3D viewport low part gradient color": "3D 视口下部渐变色",
    "3D viewport up part gradient color": "3D 视口上部渐变色",
    "A dialog to help you manage your geometry, it can help you group, tile, and select parts of your mesh":
        "用于管理几何体的对话框，可帮助你分组、分块并选择网格的各个部分。",
    "About using Map Rez, Spacing and Margin parameters:": "关于贴图分辨率、间距与边距参数：",
    "About using Regular Pack and Pack Translate:": "关于普通排布与平移排布：",
    "Absolute Stretch : Polygon color from the polygon stretch (UV polygon area over 3D polygon area)":
        "绝对拉伸：多边形颜色取自多边形拉伸度（UV 面积 / 3D 面积）",
    "Absolute value of the point snapping distance.": "点吸附距离的绝对值。",
    "Activate Link holes to link the mesh's holes using path of edges (recommended especially for meshes that come from photogrammetry).":
        "启用「连接孔洞」可用边路径连接网格的孔洞（尤其推荐用于摄影测量生成的网格）。",
    "Activate Select handle to remove higher topologies genus automatically (recommended in most cases).":
        "启用「选择把手」可自动移除高阶拓扑亏格（多数情况下推荐）。",
    "Activate the Size Limiter when you get too much long/bigger islands comparatively to the others. Long islands can make the packing unable to utilize efficiently the UV area since they form an island stack not square.":
        "当出现明显比其他岛更长/更大的岛时，启用尺寸限制。长条岛会形成非方形的岛堆叠，导致排布无法高效利用 UV 区域。",
    "Activate the Smooth when dealing with scanned meshes that have many small useless details that you don't want to be separated from the rest of the mesh. Note that smooth influence can be controlled using the protect/attract map.":
        "处理扫描网格时，若有许多不希望从主体分离的细碎无用细节，可启用平滑。平滑的影响范围可通过保护/吸引图控制。",
    "Activate the Stretch Control if you want to remove excessive stretching and angle distortion that remains after the main seam tool algorithm segmentation. The downside of that option is it creates more cut, sometimes oversegmentation.":
        "若想消除主接缝算法分割后残留的过度拉伸与角度畸变，可启用拉伸控制。缺点是会产生更多切割，有时会过度分割。",
    "Activate the frame rate display": "启用帧率显示",
    "Add current color to palette": "将当前颜色添加到调色板",
    "Additional Grid Subdivision Count": "附加网格细分数量",
    "Additional subdivision applied on the current grid. For instance, if the value is 10, the current grid will be divided by 10, after the current grid subdivision.":
        "在当前网格上追加的细分。例如值为 10 时，当前网格会在原有细分基础上再等分为 10 份。",
    "Alight Straighten Flip Fit to Grid Stack": "对齐 拉直 翻转 适配网格 堆叠",
    "Align island(s) horizontally using what is selected.": "以当前选中内容为基准水平对齐岛。",
    "Align island(s) vertically using what is selected.": "以当前选中内容为基准垂直对齐岛。",
    "Align selected elements bottom": "将选中元素底部对齐",
    "Align selected elements horizontally": "水平对齐选中元素",
    "Align selected elements left": "将选中元素左对齐",
    "Align selected elements right": "将选中元素右对齐",
    "Align selected elements top": "将选中元素顶部对齐",
    "Align selected elements vertically": "垂直对齐选中元素",
    "Aligns (cut) island(s) to matching edges. This means that if you cut an island in two, and you select one edge, clicking this button will bring the opposite island's matching edge close to the selected one. This only works on the edges on the boundaries of an island, and not inside an island":
        "将（已切割的）岛对齐到匹配边。也就是说，如果把一个岛切成两半并选中其中一条边，点击此按钮会让另一侧岛的匹配边贴近所选边。仅对岛边界上的边有效，对岛内部的边无效。",
    "Aligns selected edges or points on a horizontal axis": "将选中的边或点对齐到水平轴",
    "Aligns selected edges or points on a vertical axis": "将选中的边或点对齐到垂直轴",
    "All islands in a group that is in stack mode will no been repacked / transformed even if they are selected. However, the group stack itself can be transformed and the contained islands will be moved using the same transformation applied to the group. It is like if they where in a box, the box move and bring what it contains.":
        "堆叠模式组内的所有岛即使被选中也不会被重新排布或变换。但组堆叠本身可以被变换，其中的岛会随之移动。可以想象它们装在一个盒子里，盒子移动时里面的东西一起移动。",
    "Allow island transformation for the packing algorithm.": "允许排布算法变换岛。",
    "Angle/Length": "角度/长度",
    "Apply Density": "应用密度",
    "Apply Density (Hotkey: Shift-Q)": "应用密度（快捷键：Shift-Q）",
    "Apply Density Uniformly": "统一应用密度",
    "Apply color to island selection": "将颜色应用到选中的岛",
    "Area max value used to filter the islands set": "用于过滤岛集合的面积上限",
    "Area min value used to filter the islands set": "用于过滤岛集合的面积下限",
    "As with Unwrap and Optimize, the packing will be applied to selected islands and groups or, if no selection is made, on all visible islands.":
        "与展开和优化相同，排布会作用于选中的岛与组；若没有选中任何内容，则作用于所有可见岛。",
    "Assigns colorID using file's material ID to visible or selected islands": "使用文件中的材质 ID 为可见岛或选中岛指定颜色 ID",
    "Assigns colorID using island group to visible or selected islands": "使用岛组为可见岛或选中岛指定颜色 ID",
    "Authorize welding of islands if their UV space maximum bounding box dimension is below the specified value": "当岛在 UV 空间中的包围盒最大尺寸低于指定值时允许焊接",
    "Authorize welding of islands if their polycount is below the specified value": "当岛的多边形数量低于指定值时允许焊接",
    "Auto Fit": "自动适配",
    "Auto Save Folder Path Browser": "浏览自动保存文件夹路径",
    "Auto Seams tool will cut then flatten the processed geometry after the edges being selected. This option makes the computation of the auto segmentation and the unfolding far more slower but gives better quality.":
        "自动接缝工具会在选边后对处理的几何体进行切割再展平。此选项会显著增加自动分割与展开的计算时间，但效果更好。",
    "Auto Seams tool will pack the processed islands after the edges being selected, island cut then flattened.":
        "自动接缝工具会在选边后对处理过的岛进行排布，即先切割再展平。",
    "Auto Select Box": "自动选择盒式",
    "Auto Select Handles": "自动选择把手",
    "Auto Select Hierarchical Pelt": "自动选择层级剥皮",
    "Auto Select Hole Links": "自动选择孔洞连接",
    "Auto Select Mosaic": "自动选择马赛克",
    "Auto Select Sharp Edges": "自动选择锐边",
    "Auto save feature save your current project into FBX file regularly.": "自动保存功能会定期将当前工程保存为 FBX 文件。",
    "Auto save feature will save the backup files into that folder.": "自动保存功能会将备份文件存入该文件夹。",
    "Auto select edges using the master selection tool and options.": "使用主选择工具及其选项自动选边。",
    "Average Normal Projection": "平均法线投影",
    "Average Normal Projection (Hotkey: Alt-U)": "平均法线投影（快捷键：Alt-U）",
    "Avg Normal": "平均法线",
    "B.Boxes": "包围盒",
    "Block/unblock view orbit (view orbit must be blocked for translation, rotation and scale editions).":
        "锁定/解锁视图环绕（平移、旋转、缩放编辑时必须锁定视图环绕）。",
    "Box Mode Off": "盒式模式：关",
    "Box Mode On": "盒式模式：开",
    "Box Projection": "盒式投影",
    "Browse External Text Editor Path": "浏览外部文本编辑器路径",
    "Browse...": "浏览...",
    "Brush pressure/opacity.": "笔刷压力/不透明度。",
    "Brush size in painting mode.": "绘制模式下的笔刷大小。",
    "Brush value.": "笔刷值。",
    "Cancel current task computation. Some long task like packing can be stopped without loosing finalized iterations.":
        "取消当前任务的计算。像排布这样的长任务可以中止，已完成的迭代不会丢失。",
    "Center View on All": "视图居中：全部",
    "Center View on the selection set. TIP: Press 'Alt-F' to center on the element which located under the mouse pointer.":
        "将视图居中到选区。提示：按 Alt-F 可居中到鼠标指针下的元素。",
    "Check Overlaps and Limit Stretch": "检查重叠并限制拉伸",
    "Check stretching and add enough cuts to ensure no flips and no overlaps once the mesh will be unfolded as a post process.":
        "检查拉伸并添加足够的切割，确保网格在后续展开时不出现翻转与重叠。",
    "CheckBoard tile count, or repetition": "棋盘格贴图块数量（重复次数）",
    "Classic Projections": "经典投影",
    "Classics": "经典",
    "Clear current selection": "清除当前选择",
    "Color ID Map : Island color defined by user using dedicated tool": "颜色 ID 图：由用户通过专用工具定义的岛颜色",
    "Color of selected elements": "选中元素的颜色",
    "Color used when applying color to island in color ID map mode.": "颜色 ID 图模式下给岛着色时使用的颜色。",
    "Colors that can be used to define the ColorID Map": "可用于定义颜色 ID 图的颜色",
    "Constrain the selected edges to be aligned when unfolding and optimizing. You need to update optimize to see the effects.":
        "展开与优化时约束选中的边保持对齐。需要重新执行优化才能看到效果。",
    "Constrain the selected edges to be horizontal when unfolding and optimizing. You need to update optimize to see the effects.":
        "展开与优化时约束选中的边保持水平。需要重新执行优化才能看到效果。",
    "Constrain the selected edges to be vertical when unfolding and optimizing. You need to update optimize to see the effects.":
        "展开与优化时约束选中的边保持垂直。需要重新执行优化才能看到效果。",
    "Constrains will force the Unfold and Optimize algorithm to respect certain constrains that you can attach to the Vertexes or Edges.":
        "约束会强制展开与优化算法遵守你附加到顶点或边上的限制条件。",
    "Convention used to display the tile id": "显示贴图块编号的约定方式",
    "Converts the current polygon selection to your current primitive type, so if you switched from Poly to Edge mode, your polygon selection would be turned into Edges.":
        "将当前多边形选择转换为当前的图元类型。例如从多边形模式切到边模式时，多边形选择会转换成边。",
    "Copies the selected UV channel data in the current set. This means you can copy full layouts between channels for further refinement.":
        "把选中的 UV 通道数据复制到当前集合。这样可以在通道之间复制完整布局以便进一步调整。",
    "Create a new group using the current island/group selection.": "用当前选中的岛/组创建新组。",
    "Creates a new UV channel in the list.": "在列表中新建一个 UV 通道。",
    "Cut and Flatten After Selecting Edges": "选边后切割并展平",
    "Define how the influence of the brush will decrease versus the brush's center distance.":
        "定义笔刷影响力随距笔刷中心距离增加而衰减的方式。",
    "Delete Unused UV Sets": "删除未使用的 UV 集",
    "Deletes the selected UV Channel from the list.": "从列表中删除选中的 UV 通道。",
    "Depending of your primitive selection mode, this option unwraps your islands, depending on whether they are selected, have a mouse-over, consist of a single island selection, or islands which have been cut but not flattened yet":
        "根据当前图元选择模式，此选项会展开岛：可针对选中的岛、鼠标悬停的岛、单个选中的岛，或已切割但尚未展平的岛。",
    "Deselect all groups.": "取消选择所有组。",
    "Details Remover Map Controlled": "细节移除：由贴图控制",
    "Details Remover Off": "细节移除：关",
    "Details Remover On": "细节移除：开",
    "Details will be selected.": "将选择细节部分。",
    "Detect overlapped island sets and create groups in stack mode for all of them.":
        "检测相互重叠的岛集合，并为它们全部创建堆叠模式的组。",
    "Disable texture display": "关闭贴图显示",
    "Disabled: No color map display in viewport": "禁用：视口中不显示颜色图",
    "Display advanced option of the auto seam algorithms.": "显示自动接缝算法的高级选项。",
    "Display flat and not flat islands.": "显示已展平与未展平的岛。",
    "Display flat islands": "显示已展平的岛",
    "Display not flat islands (i.e: islands that are not yet unfolded)": "显示未展平的岛（即尚未展开的岛）",
    "Distortion Energy Based Mode": "基于畸变能量的模式",
    "Distribute Space Pixel Interval Value": "等距分布的像素间隔值",
    "Distribute Space Real Interval Value": "等距分布的实际间隔值",
    "Distributes features groups connected set of primitives. Turn this on especially when you are in Point Mode and want your vertices to move uniformly. When disabled, each vertex will be moved independently.":
        "按相连的图元组进行分布。在点模式下希望顶点整体移动时尤其应开启。关闭时每个顶点各自独立移动。",
    "Distributes your selection horizontally to the left": "将选区向左水平分布",
    "Distributes your selection horizontally to the right.": "将选区向右水平分布。",
    "Distributes your selection on a horizontally spaced axis.": "在水平方向上按等距分布选区。",
    "Distributes your selection on a vertically spaced axis.": "在垂直方向上按等距分布选区。",
    "Distributes your selection to a common horizontal center.": "将选区分布到同一水平中心线。",
    "Distributes your selection to a common vertical center.": "将选区分布到同一垂直中心线。",
    "Distributes your selection vertically to the bottom.": "将选区向下垂直分布。",
    "Distributes your selection vertically to the top": "将选区向上垂直分布",
    "Edge Based Symmetry Detection": "基于边的对称检测",
    "Edge Loop Path Geometry Based Mode": "边循环路径：基于几何模式",
    "Edge Loop Path Iteration No limit": "边循环路径：迭代次数不限",
    "Edge Loop Path Max Angle": "边循环路径最大角度",
    "Edge Loop Path Max Angle No limit": "边循环路径最大角度不限",
    "Edge Loop Stop At Selection Mode": "边循环：遇到已选边即停止",
    "Edges that have their polygon's normals forming an angle superior to this value will be selected":
        "相邻多边形法线夹角大于此值的边将被选中",
    "Edit Mode Toolbar": "编辑模式工具栏",
    "Enable Auto Deselected After isolate": "孤立后自动取消选择",
    "Enable Max Absolute Angle to select planar shapes. The more the angle is high, the more you will select polygons. Try small values before and augment the value until you get enough selected polygons.":
        "启用最大绝对角度以选择平面形状。角度越大选中的多边形越多。建议先从小值开始，逐步加大直到选到足够的多边形。",
    "Enable Partial UV Sets": "启用部分 UV 集",
    "Enable Proportional Falloff Edit": "启用比例衰减编辑",
    "Enable max absolute angle when propagating polygon selection": "传播多边形选择时启用最大绝对角度",
    "Enable max deviation angle when propagating polygon selection": "传播多边形选择时启用最大偏差角度",
    "Enable or disable ray casting for brush painting actions.": "启用或禁用笔刷绘制时的射线投射。",
    "Enable or disable the influence of normal for brush painting actions.": "启用或禁用笔刷绘制时法线的影响。",
    "Enable proportional falloff edition. When activated, the transformations will by softly propagated to the connected primitives around a distance set by \"Falloff\", with an attenuation curve: The \"Falloff Profile\".":
        "启用比例衰减编辑。启用后，变换会以「衰减」设定的距离为范围，按「衰减轮廓」曲线平滑地传播到相连的图元。",
    "Enable the Real time optimize engine. The R.T.O engine will help to reduce stretching by applying some optimize iterations on islands while you deform them using rotate scale translate or any drag spread pinch operations.":
        "启用实时优化引擎。实时优化会在你旋转、缩放、平移或拖拽、扩散、收缩时对岛执行若干次优化迭代，从而减少拉伸。",
    "Enable the proportional mode, then select some points / edges / polygons, then transform them using the available transforms tools (see the Transform Panel for that) then primitives around the selection will be moved as well according to their distance to the selection set.":
        "启用比例模式，选中一些点/边/多边形，再用变换工具（见变换面板）变换它们，周围的图元会按与选区的距离一同移动。",
    "Enable tile margin snapping.": "启用贴图块边距吸附。",
    "Enable/Disable \"Pin Map\" for Proportional Edit. When enabled, the more the vertexes are dark the less they will be transformed. Disabling it allows you to displace the pinned primitives without having to clear the Pin map.":
        "为比例编辑启用/禁用「固定图」。启用时顶点越暗受影响越小。禁用后可以在不清除固定图的情况下移动被固定的图元。",
    "Enable/Disable \"Pin Map\". When enabled, the more the vertexes are dark the less they will be transformed. Disabling it allows you to displace the pinned primitives without having to clear the Pin map.":
        "启用/禁用「固定图」。启用时顶点越暗受影响越小。禁用后可以在不清除固定图的情况下移动被固定的图元。",
    "Enable/Disable Auto isolate islands mode. When on, islands which haven't any edge selected will be automatically hidden.":
        "启用/禁用自动孤立岛模式。开启后，没有任何边被选中的岛会被自动隐藏。",
    "Enable/Disable Lighting": "启用/禁用光照",
    "Enable/Disable Pin Map For Local Brush Tools": "为局部笔刷工具启用/禁用固定图",
    "Enable/Disable Pin Map Primitive For Proportional Mode": "为比例模式启用/禁用图元固定图",
    "Enable/Disable texture decal for both viewport": "为两个视口启用/禁用贴图贴花",
    "Enables edge count for your edge loop selection.": "为边循环选择启用边数限制。",
    "Export FBX files for Autodesk Products 2010 (FBX 6.1).": "导出兼容 Autodesk 2010 产品的 FBX 文件（FBX 6.1）。",
    "Export FBX files for Autodesk Products 2011 (FBX 7.1).": "导出兼容 Autodesk 2011 产品的 FBX 文件（FBX 7.1）。",
    "Export FBX files for Autodesk Products 2012 (FBX 7.2).": "导出兼容 Autodesk 2012 产品的 FBX 文件（FBX 7.2）。",
    "Export FBX files for Autodesk Products 2013 (FBX 7.3).": "导出兼容 Autodesk 2013 产品的 FBX 文件（FBX 7.3）。",
    "Export FBX files for Autodesk Products 2014/2015 (FBX 7.4).": "导出兼容 Autodesk 2014/2015 产品的 FBX 文件（FBX 7.4）。",
    "Export FBX files for Autodesk Products 2016 (FBX 7.5).": "导出兼容 Autodesk 2016 产品的 FBX 文件（FBX 7.5）。",
    "Export FBX files for Autodesk Products 2017/2018.": "导出兼容 Autodesk 2017/2018 产品的 FBX 文件。",
    "Export Import Tile and Island Related Data": "导出/导入贴图块与岛相关数据",
    "Export and import tile, island related data such as island groups and island packing properties.":
        "导出与导入贴图块、岛相关数据，例如岛组与岛排布属性。",
    "Exporter": "导出器",
    "Extreme number of cuts, very low distortion": "极多切割，极低畸变",
    "FBX compatibility version": "FBX 兼容版本",
    "File suffix added when saving file.": "保存文件时追加的后缀。",
    "Fit Multi Enable": "启用多选适配",
    "Fit to grid will fit your primitives to your map's pixel resolution via the Layout Panel's->Map Rez setting instead of the default or defined grid":
        "适配网格会按「布局面板 → 贴图分辨率」的像素精度来适配图元，而不是按默认或自定义网格。",
    "Fits the bounding box of your selected primitives to the grid. This option will potentially enlarge your primitives when fitting them to the grid.":
        "将选中图元的包围盒适配到网格。此选项可能放大图元。",
    "Fits the bounding box of your selected primitives to the grid. This option will potentially shrink or grow your primitives when fitting them to the grid, as they will be set to fit the grid closest to them.":
        "将选中图元的包围盒适配到网格。此选项可能缩小或放大图元，因为会适配到最接近的网格。",
    "Fits the bounding box of your selected primitives to the grid. This option will potentially shrink your primitives when fitting them to the grid.":
        "将选中图元的包围盒适配到网格。此选项可能缩小图元。",
    "Flattening algorithm used.": "所使用的展平算法。",
    "Flip the selection horizontally": "水平翻转选区",
    "Flip the selection horizontally using the left side of the bounding box as flip axis": "以包围盒左侧为轴水平翻转选区",
    "Flip the selection horizontally using the right side of the bounding box as flip axis": "以包围盒右侧为轴水平翻转选区",
    "Flip the selection vertically": "垂直翻转选区",
    "Flip the selection vertically using the bottom side of the bounding box as flip axis": "以包围盒底边为轴垂直翻转选区",
    "Flip the selection vertically using the top side of the bounding box as flip axis": "以包围盒顶边为轴垂直翻转选区",
    "Follow Average Texel Density": "跟随平均纹素密度",
    "For more information - https://www.youtube.com/watch?v=Q_KkyG-X2r8": "更多信息：https://www.youtube.com/watch?v=Q_KkyG-X2r8",
    "Forbid island transformation for the packing algorithm.": "禁止排布算法变换岛。",
    "Generate some distortion and average number of cuts": "产生一定畸变，切割数量适中",
    "Grid Snap": "网格吸附",
    "Grid Subdiv U": "网格细分 U",
    "Grid Subdiv V": "网格细分 V",
    "Grid subdivision in the U direction.": "U 方向的网格细分。",
    "Grid subdivision in the V direction.": "V 方向的网格细分。",
    "Group Stack (Group in stack mode):": "组堆叠（堆叠模式组）：",
    "Group selected island in stack mode. Use that feature when you want to group and stack non-similar islands. Any island in Group Stack will never be transformed again within the Group Stack, even if they are selected.":
        "将选中的岛以堆叠模式成组。需要把不相似的岛分组并堆叠时使用。组堆叠中的岛即使被选中也不会再被变换。",
    "Groups": "组",
    "Grow  (Hotkey: KP_ADD)": "扩展选择（快捷键：小键盘 +）",
    "Grow polygon/edge/point selection": "扩展多边形/边/点选择",
    "Hide selected islands or the island under the mouse.": "隐藏选中的岛或鼠标下的岛。",
    "Hierarchical segmentation will select the branche's sections": "层级分割会选中枝干段",
    "Hierarchical segmentation will select the edges as a pelter would do it": "层级分割会像剥皮算法那样选边",
    "Hierarchical segmentation will select the leaf's sections": "层级分割会选中叶片段",
    "Hierarchical segmentation will select the trunk's sections": "层级分割会选中主干段",
    "High number of cuts, low distortion": "较多切割，低畸变",
    "High settings make the computation long or even very long, but creates better UV area coverage especially in presence of very small islands.":
        "较高设置会让计算变长甚至非常长，但能获得更好的 UV 区域利用率，尤其在存在很小的岛时。",
    "High values give less stretching and angle distortion but select more edges (more islands count after cut).":
        "值越大拉伸与角度畸变越小，但会选中更多边（切割后岛的数量更多）。",
    "High values will segment more so the islands will be unfolded with less distortion. Low values will segment less but the cut will generate more distortion.":
        "值越大分割越多，展开后畸变越小。值越小分割越少，但切割会带来更多畸变。",
    "If an island on your mesh has been given several cuts, Weld Self Island will weld these back independently, without welding across islands. It will only weld the island and its cuts. Use this when you want to get rid of some bad cuts or want to avoid a reset.":
        "如果网格上的某个岛被切了多刀，「焊接自身岛」会把这些切口各自焊回，不会跨岛焊接。它只焊接该岛及其切口。想消除不良切割或避免重置时使用。",
    "If enabled, UV sets that have zero flattened polygons will not be exported in the file. In presence of multiple UV sets, if such a completely not flattened UV set would be located in the first UV Channel, the second UV channel (flattened) will be placed in the first one!":
        "启用后，不含任何已展平多边形的 UV 集不会被导出。若存在多个 UV 集，而第一个通道恰好是完全未展平的 UV 集，则第二个（已展平的）UV 通道会被放到第一位！",
    "If enabled, island will be automatically deselected after an isolate action": "启用后，执行孤立操作后岛会自动取消选择",
    "If enabled, non flat polygons and their associated UV nodes will not be exported. Warning: this options may not be compatible with all 3D Software.":
        "启用后，未展平的多边形及其关联 UV 节点不会被导出。警告：此选项可能不兼容所有 3D 软件。",
    "If enabled, the UV Sets ordering will be kept for all meshes present in the FBX file. If disabled, the UV Set order displayed in RizomUV will be used to recreate all UV Sets in the file.":
        "启用后，FBX 文件中所有网格的 UV 集顺序会被保留。禁用后，将按 RizomUV 中显示的 UV 集顺序重建文件中的所有 UV 集。",
    "If no scene unit is defined in the model file, which is always the case with OBJ files, this value will be used as default.":
        "如果模型文件中未定义场景单位（OBJ 文件总是如此），则使用此默认值。",
    "If you have cut your mesh into several islands, Weld Across Islands will weld these back together. Use this when you want to weld specific islands back together and/or want to avoid a reset.":
        "如果把网格切成了多个岛，「跨岛焊接」会把它们重新焊在一起。想把特定岛焊回一起或想避免重置时使用。",
    "If you have some islands that are not similar, but you want them to keep their position / rotation / scale relatively to other islands of the group, you can use the Group Stack button. The islands will keep their current transformation and be grouped in a Group Stack.":
        "如果有一些并不相似的岛，但希望它们相对组内其他岛保持位置/旋转/缩放，可以使用「组堆叠」按钮。这些岛会保留当前变换并被归入组堆叠。",
    "If you have some islands that are similars (i.e same topology and same shape in 3D), they are good candidate to be stacked in the diffuse map. You can use Stack & Group Stack button for them. It will stack the similar islands over each other, then put them in a new Group Stack.":
        "如果有一些相似的岛（即 3D 中拓扑与形状相同），它们很适合在漫反射贴图中堆叠。可以使用「堆叠并分组相似岛」按钮：先把相似的岛互相堆叠，再放入新的组堆叠。",
    "Import...": "导入...",
    "Impose equality between U and V Texture Tiling Factor.": "强制 U 与 V 的贴图平铺系数相等。",
    "In Tile mode The flipping axis will be determined by the tile geometry that contains the current selection. In Local mode, the flipping will be applied independently each primitive groups or by island. In Global mode, the flipping will be applied to the global selection set like it would be a single part.":
        "贴图块模式下，翻转轴由包含当前选区的贴图块几何决定。局部模式下，翻转会按图元组或按岛独立进行。全局模式下，翻转会把整个选区当作一个整体处理。",
    "In addition to iterations count, you can also choose how strong you want these to be. Setting the slider to 0 will have zero effect, whereas 1 - one - will have it on full strength.":
        "除迭代次数外，还可以选择作用强度。滑块设为 0 时无效果，设为 1 时为满强度。",
    "In all primitive selection modes (point/edge/polygons/island), pressing the 'D' key + mouse buttons will transform the island which is under the mouse pointer.":
        "在所有图元选择模式（点/边/多边形/岛）下，按 D 键加鼠标键可变换鼠标指针下的岛。",
    "In case of noisy meshes or some hard surface meshes that have some bevels, adding some smooth iterations will give you cleaner polygon selection sets":
        "对于噪点较多的网格或带有倒角的硬表面网格，增加一些平滑迭代可以得到更干净的多边形选择集。",
    "Initial Orientation": "初始朝向",
    "Initial Scale": "初始缩放",
    "Isl. Group": "岛组",
    "Island Groups allow you to gather set of island.": "岛组用于把一组岛聚合在一起。",
    "Island Groups can be simply used to classify some of your islands because you want to isolate them from the rest of the whole mesh model, or they can be used to specify to the packing algorithm that you want them placed together in the UV space. To create a group, select some islands then press 'G'.":
        "岛组既可以单纯用于分类，把某些岛从整个网格模型中分离出来；也可以用来告诉排布算法你希望它们被放在 UV 空间的相邻位置。创建组的方法是选中若干岛后按 G。",
    "Island Spacing": "岛间距",
    "Island Stretch : Polygon color from the polygon normalized stretch (UV polygon area over 3D polygon area normalized by island stretch)":
        "岛拉伸：多边形颜色取自归一化拉伸（UV 面积 / 3D 面积，再按岛拉伸归一化）",
    "Island orientation optimization disabled.": "已禁用岛朝向优化。",
    "Island visibility controls the visibility of the islands in the viewport but also determines which islands will be processed by the algorithms. As a general rule hidden islands will not be processed. However hidden islands will be saved into files even if they are not visible in the viewport.":
        "岛可见性既控制视口中的显示，也决定哪些岛会被算法处理。通常隐藏的岛不会被处理，但仍会被保存到文件中。",
    "Islands in the group will not be repacked, even if recursive packing is enabled. This allows islands to be, and keep being stacked on top of each other.":
        "组内的岛不会被重新排布，即使启用了递归排布。这样岛可以持续保持互相堆叠。",
    "Islands of the group will be repacked if recursive packing is enabled.": "如果启用递归排布，组内的岛会被重新排布。",
    "Keep Average Texel Density": "保持平均纹素密度",
    "Keep islands that have a higher area than the value specified. You can define this via the slider, or enter the value in the spinner.":
        "保留面积大于指定值的岛。可通过滑块设定，或在数值框中输入。",
    "Keep islands that have a lesser area than the value specified. You can define this via the slider, or enter the value in the spinner. .":
        "保留面积小于指定值的岛。可通过滑块设定，或在数值框中输入。",
    "Keep islands that have less than the specified number of polygons. You can define this via the slider, or enter the value in the spinner.":
        "保留多边形数量少于指定值的岛。可通过滑块设定，或在数值框中输入。",
    "Keep islands that have more than the specified number of polygons. You can define this via the slider, or enter the value in the spinner.":
        "保留多边形数量多于指定值的岛。可通过滑块设定，或在数值框中输入。",
    "Keep will not do anything to resize the islands being packed.": "「保持」不会改变被排布的岛的大小。",
    "Labels": "标签",
    "Launch browser to the official RizomUV downloading page...": "用浏览器打开 RizomUV 官方下载页面...",
    "Launch browser to the official RizomUV support page...": "用浏览器打开 RizomUV 官方支持页面...",
    "Launch registered LUA script files (.lua)": "运行已注册的 LUA 脚本文件（.lua）",
    "Layout Texel Density": "布局纹素密度",
    "Layout Texel Density Display": "布局纹素密度显示",
    "Layout texel density": "布局纹素密度",
    "Lets you define the maximum amount of edges that will select themselves for edge loop propagation.":
        "设定边循环传播时自动选中的最大边数。",
    "Lets you define the maximum angle between two edges to allow edge selection propagation. Setting the angle to 180 effectively disables this.":
        "设定允许选择传播的两条边之间的最大夹角。设为 180 即等于禁用此限制。",
    "Lets you set the maximum angle to 180, ensuring there is no limit to the edge loop selection propagation.":
        "将最大角度设为 180，使边循环选择传播不受角度限制。",
    "Lets you set the maximum angle when trying to find the best orientation for the packing algorithm.":
        "设定排布算法寻找最佳朝向时的最大角度。",
    "Lets you set the starting angle (offset) when trying to find the best orientation for the packing algorithm.":
        "设定排布算法寻找最佳朝向时的起始角度（偏移）。",
    "Link U and V Texture Tiling Factor by the current ratio.": "按当前比例链接 U 与 V 的贴图平铺系数。",
    "Link all holes and frontiers with path of edges.": "用边路径连接所有孔洞与边界。",
    "Live Cut Mode": "实时切割模式",
    "Low number of cuts, but will generate distortion": "较少切割，但会产生畸变",
    "Magnet Weld welds edges that are superposed, or in very close proximity to each other in UV Space - aka the 2D view. You control the distance at which they weld by adjusting the values in the Magnet Weld spinner.":
        "磁性焊接会在 UV 空间（即 2D 视图）中焊接重合或非常接近的边。焊接距离通过磁性焊接数值框调整。",
    "Main Toolbar": "主工具栏",
    "Make the selected polygons rectangular": "将选中的多边形变为矩形",
    "Make the selected polygons rectangular then orient the result horizontally": "将选中的多边形变为矩形并水平摆放",
    "Make the selected polygons rectangular then orient the result vertically": "将选中的多边形变为矩形并垂直摆放",
    "Make the selected vertex(es) become hinge(s). PLEASE NOTE: This has only an influence if the hinge is located between two consecutive edges that have Edge Aligned Constraints. You need to update optimize to see the effects.":
        "将选中的顶点设为铰链。请注意：只有当铰链位于两条带「边对齐约束」的相邻边之间时才有效。需要重新执行优化才能看到效果。",
    "Manual: The range is determined using user specified values.": "手动：范围由用户指定的数值决定。",
    "Map": "贴图",
    "Map Resolution": "贴图分辨率",
    "Margin Snap": "边距吸附",
    "Master Seam Tool Options": "主接缝工具选项",
    "Master Seam Tool Selector": "主接缝工具选择器",
    "Match Specified Texel Density": "匹配指定纹素密度",
    "Material ID : Polygon color from the file's material ID": "材质 ID：多边形颜色取自文件中的材质 ID",
    "Max Angle Unset": "最大角度：未设定",
    "Max Deviation Normal (Shift+MouseWheel)": "最大偏差法线（Shift+滚轮）",
    "Max Deviation Normal Angle (Planar Shapes)": "最大偏差法线角度（平面形状）",
    "Max Deviation Normal Enable": "启用最大偏差法线",
    "Max Edge Angle (Alt+MouseWheel)": "最大边角度（Alt+滚轮）",
    "Max Edge Angle (Curved Shapes)": "最大边角度（曲面形状）",
    "Max Edge Angle Enable": "启用最大边角度",
    "Max angle value of the selected elements is determined by the global packing setting.":
        "选中元素的最大角度值由全局排布设置决定。",
    "Maximum Mutations": "最大变异次数",
    "Maximum allowed ratio of the bounding box length over the average of the maximum bounding box length of all islands. Low values create many cuts, wigh values create less cuts.":
        "允许的包围盒长度与所有岛最大包围盒长度平均值之比的上限。值越小切割越多，值越大切割越少。",
    "Maximum angle between the selected polygon normals and the others that allow them to be selected. 0 will select coplanar polygons only, 180 will select all polygons":
        "选中多边形法线与其他多边形法线之间允许被选中的最大夹角。0 只选共面多边形，180 选全部多边形。",
    "Maximum angle between two polygons that allow the selection to be propagated. 0 will select coplanar polygons only, 180 will select all polygons":
        "允许选择传播的两个多边形之间的最大夹角。0 只选共面多边形，180 选全部多边形。",
    "Maximum distance that allow the weld magnet feature to weld two opposite edges.":
        "磁性焊接功能允许焊接两条相对边的最大距离。",
    "Maximum number of trial to find best packing solution (press stop button to stop the computations). The more islands there is the less useful high values are.":
        "寻找最佳排布方案的最大尝试次数（按停止按钮可中止计算）。岛越多，高数值的作用越小。",
    "Maximum relative distance between two edge that allows them to be welded. The distance is relative to the average edge length.":
        "允许两条边焊接的最大相对距离，该距离相对于平均边长。",
    "Mesh wire color when polygons are displayed": "显示多边形时的网格线框颜色",
    "Mesh wire color when polygons are displayed and the edge is the primitive selection mode": "显示多边形且处于边图元模式时的网格线框颜色",
    "Mesh wire color when polygons are not displayed": "不显示多边形时的网格线框颜色",
    "Mesh's borders color": "网格边界颜色",
    "Min Angle Unset": "最小角度：未设定",
    "Min angle value of the selected elements is determined by the global packing setting.":
        "选中元素的最小角度值由全局排布设置决定。",
    "Minimum Hole Size": "最小孔洞尺寸",
    "Minimum size of the isolated polygon groups (in polygons). If the size is superior to zero, unselected polygon groups surrounded by selected ones will be automatically selected even if they are above angles tolerances":
        "孤立多边形组的最小尺寸（以多边形计）。若大于 0，被选中多边形包围的未选中多边形组即使超出角度容差也会被自动选中。",
    "Mix value of the smoothing step applied before selecting polygons": "选多边形前所执行平滑步骤的混合值",
    "Mosaic segmentation will not automatically determines the island count for each island to segment but use the specified value.":
        "马赛克分割不会自动决定每个岛的分割数量，而是使用指定的数值。",
    "Move the opposite island so that it stick to the selected edge before welding it.":
        "焊接前先将对面的岛移动贴合到所选边。",
    "Near plane clipping distance to eye. Lowest values can create artifacts (z-fighting)":
        "近裁剪面到视点的距离。数值过低会产生伪影（Z 冲突）。",
    "Neutral: The range will be adapted so that the neutral color matches the Layout->TargetDensity value.":
        "中性：范围会自动调整，使中性色对应「布局 → 目标密度」的值。",
    "Note :": "注意：",
    "Number of columns of the multi UV tiles.": "多 UV 贴图块的列数。",
    "Number of iteration for the optimize algorithm.": "优化算法的迭代次数。",
    "Number of iterations when deforming mesh. More iteration bring better results, but the computation is slower.":
        "变形网格时的迭代次数。迭代越多效果越好，但计算更慢。",
    "Number of optimize iterations added after an unfold operation.": "展开操作后追加的优化迭代次数。",
    "Number of parts in which each island must be segmented into.": "每个岛需要分割成的份数。",
    "Number of rows of UV the multi UV tiles.": "多 UV 贴图块的行数。",
    "Once the islands are inside a group, you can pack them within the group by selecting them (double click one of them), then use the pack feature.":
        "岛进入组之后，可以选中它们（双击其中一个）再使用排布功能，在组内排布。",
    "Once the packing finishes, AutoFit rescales all island sets to best fit inside the tile.":
        "排布完成后，自动适配会重新缩放所有岛集合，使其最佳地适配贴图块。",
    "Once you defined your colors, open the exported dialog (Ctrl-N), enable one of the Stamp channel, enable ColorIDMap polygon rendering mode, then click on the Export enabled files button":
        "定义好颜色后，打开导出对话框（Ctrl-N），启用其中一个输出通道，选择 ColorIDMap 多边形渲染模式，然后点击「导出已启用的文件」。",
    "Once you've picked or set your Texel Density, clicking the Apply Density icon scales selected islands to the specified texel density.":
        "取用或设定纹素密度后，点击「应用密度」图标会把选中的岛缩放到指定的纹素密度。",
    "Once you've picked or set your Texel Density, clicking the Set Density Uniformly icon uniformly scales selected islands to the average of the specified density.":
        "取用或设定纹素密度后，点击「统一设置密度」图标会把选中的岛统一缩放到指定密度的平均值。",
    "Open Debug Log File Path Location": "打开调试日志所在位置",
    "Open the debug log file folder using the file explorer.": "用文件资源管理器打开调试日志文件夹。",
    "Open the keyboard and mouse customizer dialog": "打开键盘与鼠标自定义对话框",
    "Opens a file selector to select a program file name.": "打开文件选择器以指定程序文件。",
    "Opens a file selector to select folder to save backup files into.": "打开文件夹选择器以指定备份文件保存位置。",
    "Optimization Lengths or Angle": "优化长度或角度",
    "Optimization force": "优化强度",
    "Optimize Iteration Count": "优化迭代次数",
    "Optimize Iteration Count After Unfold": "展开后的优化迭代次数",
    "Order UV Set by Names": "按名称排序 UV 集",
    "Orient the view so that the selected vector is Up and use appropriate rotation axises":
        "调整视图方向，使所选向量朝上，并采用相应的旋转轴。",
    "Orientation Optimization": "朝向优化",
    "Outlines": "轮廓",
    "Overlapped": "重叠",
    "PLEASE NOTE: if this option is enabled, even the locked islands will be moved, and the texel density of the islands will be modified.":
        "请注意：启用此选项后，连锁定的岛也会被移动，岛的纹素密度也会改变。",
    "Pack After Select Edges": "选边后执行排布",
    "Pack Algorithm Accuracy": "排布算法精度",
    "Pack All": "排布全部",
    "Pack all island groups hierarchy before packing the full layout.": "在排布整体布局之前，先按层级排布所有岛组。",
    "Packing Texel Density": "排布纹素密度",
    "Packs selected or all islands if none are selected, but keeps their current orientation and scale":
        "排布选中的岛；若未选中则排布全部岛，但保持其当前朝向与缩放。",
    "Packs selected, or all islands if none are selected": "排布选中的岛；若未选中则排布全部岛",
    "Pick Density": "拾取密度",
    "Pick Density (Hotkey: Alt-Q)": "拾取密度（快捷键：Alt-Q）",
    "Pick Density For Packing": "为排布拾取密度",
    "Pick color from island selection": "从选中的岛拾取颜色",
    "Pin Selected point(s) or edge(s) or face(s)": "固定选中的点、边或面",
    "Pixels units Mode": "像素单位模式",
    "Please Note : If you are going to define multiple channels for your model, remember to save in FBX, as the OBJ format is not capable of handling multiple UV channels.":
        "请注意：如果要为模型定义多个通道，请务必保存为 FBX，因为 OBJ 格式无法处理多个 UV 通道。",
    "Please Note : Unlike Stack and Group Similar, this option will not Group the stack at the end of the operation.":
        "请注意：与「堆叠并分组相似岛」不同，此选项不会在操作结束时把堆叠结果成组。",
    "Please note that as of this release, CTRL + M is obsolete.": "请注意，自本版本起 CTRL + M 已废弃。",
    "Point Snap": "点吸附",
    "Point Snap Absolute Distance": "点吸附绝对距离",
    "Polygon count max value used to filter the islands set": "用于过滤岛集合的多边形数量上限",
    "Polygon count min value used to filter the islands set": "用于过滤岛集合的多边形数量下限",
    "Pre-orient the island(s) horizontally before packing (using its bounding box).": "排布前（按包围盒）将岛预先水平摆正。",
    "Pre-orient the island(s) so that their X-axis in 3D space aligns to the V axis in UV Space":
        "排布前将岛预摆正，使其 3D 空间中的 X 轴对齐 UV 空间的 V 轴。",
    "Pre-orient the island(s) so that their Y-axis in 3D space aligns to the V axis in UV Space":
        "排布前将岛预摆正，使其 3D 空间中的 Y 轴对齐 UV 空间的 V 轴。",
    "Pre-orient the island(s) so that their Z-axis in 3D space aligns to the V axis in UV Space":
        "排布前将岛预摆正，使其 3D 空间中的 Z 轴对齐 UV 空间的 V 轴。",
    "Pre-orient the island(s) vertically before packing (using its bounding box).": "排布前（按包围盒）将岛预先垂直摆正。",
    "Project 3D geometry on the 6 faces of a cube. Tip: use AutoSeam Box Tool to well prepare the cut of the object before.":
        "将 3D 几何体投影到立方体的 6 个面上。提示：先用自动接缝的盒式工具准备好对象切割。",
    "Project 3D geometry using the average normal of each islands or each isolated group of selected primitives. Applied on selection if not empty or on everything in the contrary case.":
        "按每个岛或每组孤立选中图元的平均法线投影 3D 几何体。有选区时作用于选区，否则作用于全部。",
    "Provided that your islands are similar enough, Select Similar copies your selection across islands with the same topology. As of version 2020.1.100, this also includes islands, the selection process is no longer limited to edges.":
        "只要岛足够相似，「选择相似岛」就会把选择复制到拓扑相同的其他岛上。自 2020.1.100 起也支持岛级选择，不再局限于边。",
    "RMB to add point, DRMB to finish, RMB to cancel, MMB to remove last point.":
        "右键添加点，双击右键完成，右键取消，中键移除上一个点。",
    "ReWeld Length Max": "重焊最大长度",
    "ReWeld Poly Max": "重焊最大多边形数",
    "Read-only layout texel density reminder display. Use the numerical text entry present in the Layout panel to change it, or enable Custom mode.":
        "只读的布局纹素密度提示显示。要修改请使用布局面板中的数值输入框，或启用自定义模式。",
    "Real Time Optimize Iteration Count": "实时优化迭代次数",
    "Recent file list open 3D instead of UVs.": "最近文件列表以 3D 模式而非 UV 模式打开。",
    "Red points indicate problem in symmetry. Use the \"wireframe displaying\" mode to easily find them in viewports.":
        "红色点表示对称存在问题。使用「线框显示」模式可在视口中轻松找到它们。",
    "Redistribute": "重新分配",
    "Redistribute evenly all active islands into active tiles before packing. If disabled, the islands will remains in their current respective tile.":
        "排布前把所有活动岛均匀重新分配到活动贴图块中。禁用后，岛会留在各自当前的贴图块中。",
    "Remove": "移除",
    "Remove selected island/group From their respective group using the current island/group selection.":
        "用当前选中的岛/组，把选中的岛/组从各自所属的组中移除。",
    "Remove the hinge constraint on selected vertexes": "移除选中顶点的铰链约束",
    "Removes constrains on selected edges. On all edges if none selected. Can also be applied on the island selection.":
        "移除选中边上的约束；若未选中则作用于全部边。也可作用于选中的岛。",
    "Rename the current UV Channel in the list.": "重命名列表中当前的 UV 通道。",
    "Rename the selected groups.": "重命名选中的组。",
    "Rescale selected Islands to fit the UV Square. PLEASE NOTE: Squarify may cause the islands to be slightly deformed. This happens as Squarify fit the islands into both UV tile dimensions":
        "重新缩放选中的岛以适配 UV 方形区域。请注意：方形化可能使岛轻微变形，因为需要同时适配 UV 贴图块的两个维度。",
    "Rescale selected islands to fit the UV Square (without deforming them)": "重新缩放选中的岛以适配 UV 方形区域（不使其变形）",
    "Rescale the selected island(s) to ensure that their UV/3D area ratio matches the current average UV/3D area ratio of the selected islands. (on selected islands, or on all islands if none selected, hidden island are ignored)":
        "重新缩放选中的岛，使其 UV/3D 面积比匹配当前选中岛的平均 UV/3D 面积比。（作用于选中的岛；若未选中则作用于全部岛，忽略隐藏岛）",
    "Reset UV tile size and offset to normalized sizes (Default UV Square).": "将 UV 贴图块尺寸与偏移重置为归一化值（默认 UV 方形）。",
    "Resize the islands so that their texel density will match the average texel density of islands that are non-selected and non-locked.":
        "调整岛的大小，使其纹素密度匹配未选中且未锁定岛的平均纹素密度。",
    "Resize the islands so they match the specified texel density value. PLEASE NOTE: If 'Autofit' is enabled, the whole tile content will be rescaled, and your specified texel density will not be kept.":
        "调整岛的大小以匹配指定的纹素密度。请注意：若启用了「自动适配」，整个贴图块的内容都会被重新缩放，指定的纹素密度将无法保持。",
    "Resizes the islands so their texel density will match the average texel density of the selected, or currently transformed islands.":
        "调整岛的大小，使其纹素密度匹配选中（或当前正在变换）岛的平均纹素密度。",
    "Room Space": "空间余量",
    "Rotate Off": "旋转：关",
    "Running Optimize on a flattened geometry will decrease distortion even more in most cases and on most islands. Depending of your primitive selection mode, this option optimizes your flattened islands, depending on whether they are selected, have a mouse-over, or consist of a single island selection":
        "对已展平的几何体执行优化，在多数情况和多数岛上能进一步降低畸变。根据当前图元选择模式，此选项会优化已展平的岛：可针对选中的岛、鼠标悬停的岛，或单个选中的岛。",
    "Scene File Unit": "场景文件单位",
    "Scene file unit. Should be defined equal to the unit of the model file. This value will be automatically set from the FBX file scene option data. But it should be specified by hand when loading OBJ file.":
        "场景文件单位。应与模型文件的单位一致。此值会从 FBX 文件的场景选项数据自动设定，但载入 OBJ 文件时需要手动指定。",
    "Select Box when dealing with simple cubic like geometry or when you want a robust result on big and dirty assets without any overlaps. In that case you may enable the Box flattening method which is available in the advanced options set.":
        "处理类似立方体的简单几何体，或希望在大型脏资产上获得无重叠的稳定结果时，请选择「盒式」。此时可在高级选项中启用盒式展平方法。",
    "Select Branches": "选择枝干",
    "Select Hierarchical Pelt algorithm when dealing with characters or threes, or more generally geometries that could be represented hierarchically or with a skeleton.":
        "处理角色、树木，或更一般地可表示为层级或骨架结构的几何体时，选择层级剥皮算法。",
    "Select Isolated Groups": "选择孤立组",
    "Select Leafs": "选择叶片",
    "Select Parallel Edges": "选择平行边",
    "Select Sharpest Edge when dealing with geometry containing many sharp edges that defines well the boundaries of the different parts of the model. Some hard surface models are good candidates for this feature.":
        "当几何体含有大量能很好界定各部件边界的锐边时，选择「最锐边」。某些硬表面模型很适合此功能。",
    "Select Trunks": "选择主干",
    "Select all": "全选",
    "Select all cylinder's and extruded shape's caps and one caps link": "选择所有圆柱与挤出形状的端盖，以及一条端盖连接线",
    "Select all groups.": "选择所有组。",
    "Select all handles of the mesh using path of edges.": "用边路径选择网格的所有把手。",
    "Select edges using the Box algorithm. Each island are projected on 6 orthogonal planes and form several polygon groups. All polygon groups frontiers are then selected.":
        "使用盒式算法选边。每个岛投影到 6 个正交平面上形成若干多边形组，随后选中所有多边形组的边界。",
    "Select edges using the Mosaic algorithm. Planar surfaces of the model will be extracted so that the mesh will be segmented into smaller parts.":
        "使用马赛克算法选边。模型的平面会被提取出来，使网格分割成更小的部分。",
    "Select edges using the sharp edges algorithm. Each edge that has their two connected polygon normals that make an angle superior to a threshold will be selected.":
        "使用锐边算法选边。两个相邻多边形法线夹角超过阈值的边会被选中。",
    "Select links between holes in the post-process step": "在后处理步骤中选择孔洞之间的连接",
    "Select points or edges located on selection's boundary": "选择位于选区边界上的点或边",
    "Select polygon set using geometric characteristics.": "按几何特征选择多边形集合。",
    "Select the handles in the post-process step": "在后处理步骤中选择把手",
    "Select the rest of the islands connected to your selection, very similar to Select Element in 3DS Max. Please Note: You can also use your middle mouse button to select, just double click.":
        "选择与当前选区相连的其余岛，类似 3DS Max 的「选择元素」。请注意：也可以用中键双击来选择。",
    "Select the visible islands that match all criteria simultaneously.": "选择同时满足所有条件的可见岛。",
    "Selects a run of loops starting from your current edge selection": "从当前选中的边开始选择一串循环边",
    "Selects all inverted polygons or inverted islands. In a UV space context, inverted means that the element's normals are facing downward in UV Space, and are shown as black.":
        "选择所有翻转的多边形或翻转的岛。在 UV 空间语境下，翻转指元素法线在 UV 空间中朝下，并显示为黑色。",
    "Selects overlapping polygons. In Island Mode (F4) it will select islands which have at least one triangle overlapping other triangles":
        "选择重叠的多边形。在岛模式（F4）下，会选中至少有一个三角形与其他三角形重叠的岛。",
    "Set Texture Tiling Ratio mode From Custom Picture": "将贴图平铺比例模式设为自定义图片",
    "Set Texture Tiling Ratio mode to 1:1": "将贴图平铺比例模式设为 1:1",
    "Set Texture Tiling Ratio mode to Free": "将贴图平铺比例模式设为自由",
    "Set Texture Tiling Ratio mode to linked": "将贴图平铺比例模式设为链接",
    "Set The Proportional Falloff Distance": "设置比例衰减距离",
    "Set The Proportional Falloff Distance to Screen Space Mode": "将比例衰减距离设为屏幕空间模式",
    "Set The Proportional Falloff Type": "设置比例衰减类型",
    "Set UV tile horizontal size": "设置 UV 贴图块水平尺寸",
    "Set UV tile vertical size": "设置 UV 贴图块垂直尺寸",
    "Set margin, island spacing and texel density in pixel unit instead of the unit defined by the Scene Unit controller.":
        "以像素为单位设置边距、岛间距与纹素密度，而非场景单位控制器定义的单位。",
    "Set the Texture Tiling Ratio From the Custom Picture.": "从自定义图片设定贴图平铺比例。",
    "Set the UV/3D area ratio to the average UV/3D area ratio of the unselected islands in each tile. (Applied on selected islands, or on all islands if none selected, hidden island are ignored)":
        "将 UV/3D 面积比设为每个贴图块中未选中岛的平均 UV/3D 面积比。（作用于选中的岛；若未选中则作用于全部岛，忽略隐藏岛）",
    "Set the proportional editing falloff curve type.": "设置比例编辑的衰减曲线类型。",
    "Set the proportional editing falloff distance.": "设置比例编辑的衰减距离。",
    "Set the proportional falloff distance to screen space mode. If active the unity of \"Falloff\" is relative to the viewport's space, if not to world space.":
        "将比例衰减距离设为屏幕空间模式。启用时「衰减」的单位相对于视口空间，否则相对于世界空间。",
    "Show / Hide the symmetry dialog.": "显示/隐藏对称对话框。",
    "Show Advanced Auto Seams": "显示高级自动接缝",
    "Show Grid": "显示网格",
    "Show a file selector that allows to select your program editor.": "打开文件选择器以选择外部编辑器程序。",
    "Show all islands": "显示所有岛",
    "Show colored bounding boxes around islands groups": "在岛组周围显示彩色包围盒",
    "Show colored outlines around islands that are inside groups": "为组内的岛显示彩色轮廓",
    "Show islands groups labels": "显示岛组标签",
    "Show this license into license account page using the default web browser": "用默认浏览器在许可账户页面中查看此许可",
    "Show transform tool when selection is not empty (Hit TAB key to display the tool whenever this button is down or not).":
        "有选区时显示变换工具（无论此按钮是否按下，按 TAB 键都可显示该工具）。",
    "Similar Symmetric will process islands which share the same topology and have inverted normal orientation including symmetric parts.":
        "「对称相似」会处理拓扑相同且法线朝向相反的岛，包括对称部件。",
    "Small details will tend to be ignored.": "细小细节将被忽略。",
    "Smooth Mix Value": "平滑混合值",
    "Smoothing (Noisy Shapes)": "平滑（噪点形状）",
    "Snap Distance Mode Absolute": "吸附距离模式：绝对",
    "Snap Distance Mode Grid": "吸附距离模式：网格",
    "Snap Distance Mode View": "吸附距离模式：视图",
    "So if you are in Point(F1), Edge(F2) Poly(F3), and Island mode(F4), use Alt + C to copy your selections.":
        "因此，在点（F1）、边（F2）、多边形（F3）或岛（F4）模式下，用 Alt + C 复制选择。",
    "Space put between items in pixel unit": "项目之间的间隔（像素单位）",
    "Space put between items in real value unit": "项目之间的间隔（实际值单位）",
    "Stack Similar copies the seams and the UV coordinates of the islands so they form a stack, provided that they have sufficient similarity.":
        "「堆叠相似岛」会复制岛的接缝与 UV 坐标，使其形成堆叠，前提是相似度足够。",
    "Stack and Group Similar copies the seams and UV coordinates of the islands into a stack, provided their similarity matches your criteria. After staking, it will then group the stacked islands in Stack Mode. Any island in a Group Stack will be immune to transformations made by the packing feature, even if it is selected or the Pack All option is enabled in the packing channel.":
        "「堆叠并分组相似岛」会复制岛的接缝与 UV 坐标形成堆叠，前提是相似度符合条件。堆叠后会把这些岛以堆叠模式成组。组堆叠中的任何岛都不会被排布功能变换，即使它被选中或排布通道中启用了「排布全部」。",
    "Stack the symmetrical parts over the master parts": "将对称部件堆叠到主侧部件之上",
    "Stack the symmetrical parts over the slave parts": "将对称部件堆叠到从侧部件之上",
    "Step Angle 180": "步进角度 180",
    "Step Angle 45": "步进角度 45",
    "Step Angle 90": "步进角度 90",
    "Step Angle Disabled": "步进角度：禁用",
    "Step Angle Unset": "步进角度：未设定",
    "Step angle for finding the best orientation for the packing algorithm.": "排布算法寻找最佳朝向时的步进角度。",
    "Step angle set at 180 degrees for defining and finding the best rotation orientation for the packing algorithm. this means some of your islands will pack horizontally.":
        "步进角度设为 180 度，用于确定并寻找排布算法的最佳旋转朝向。这意味着部分岛会水平排布。",
    "Step angle set at 45 degrees for defining and finding the best rotation orientation for the packing algorithm. This means some of your islands will pack at a 45-degree angle.":
        "步进角度设为 45 度，用于确定并寻找排布算法的最佳旋转朝向。这意味着部分岛会以 45 度角排布。",
    "Step angle set at 90 degrees for defining and finding the best rotation orientation for the packing algorithm. This means some of your islands will pack vertically..":
        "步进角度设为 90 度，用于确定并寻找排布算法的最佳旋转朝向。这意味着部分岛会垂直排布。",
    "Step angle value of the selected elements is determined by the global packing setting.":
        "选中元素的步进角度值由全局排布设置决定。",
    "Stops selecting edges when coming across an already selected edge.": "遇到已选中的边时停止继续选边。",
    "Straighten selected points or edges": "拉直选中的点或边",
    "Switch UV and 3D viewport visibility": "切换 UV 与 3D 视口的显示",
    "Switch from perspective mode to orthographic mode": "在透视模式与正交模式之间切换",
    "Switch on/off background pic in uv quad": "开关 UV 方形区域中的背景图片",
    "Switch on/off borders/seams visibility. Be careful when disabled, you will not see the effect of cut operations, which can be error prone.":
        "开关边界/接缝显示。禁用后看不到切割操作的效果，容易出错，请谨慎使用。",
    "Switch to edge edit mode": "切换到边编辑模式",
    "Switch to edit mode brush pin map": "切换到笔刷固定图编辑模式",
    "Switch to edit mode drag": "切换到拖拽编辑模式",
    "Switch to edit mode paint protect/attract map": "切换到保护/吸引图绘制编辑模式",
    "Switch to edit mode pinch": "切换到收缩编辑模式",
    "Switch to edit mode selection (TIP: Press TAB + LMB for rapid access to Trans/Rot/Scal gizmo)":
        "切换到选择编辑模式（提示：按 TAB + 左键可快速调出平移/旋转/缩放操纵器）",
    "Switch to edit mode spread": "切换到扩散编辑模式",
    "Switch to island edit mode": "切换到岛编辑模式",
    "Switch to point edit mode": "切换到点编辑模式",
    "Switch to polygon edit mode": "切换到多边形编辑模式",
    "TIP: You can select all islands within a group at a time by double clicking on one of them. It is then super easy to move them tightly.":
        "提示：双击组内任意一个岛即可一次选中组内所有岛，这样就能很方便地整体紧密移动。",
    "Texel Density : Polygon color from texel density": "纹素密度：多边形颜色取自纹素密度",
    "Texel Density Unit": "纹素密度单位",
    "Texel density map lower bound": "纹素密度图下限",
    "Texel density map upper bound": "纹素密度图上限",
    "Texel density unit. Most common value is texel per centimeter (tx/cm)": "纹素密度单位。最常用的是每厘米纹素数（tx/cm）。",
    "Texture Multiplier U": "贴图倍增 U",
    "Texture Multiplier V": "贴图倍增 V",
    "Texture multiplier U value. Tip: Use PageDown and PageUp keys to change the values using the keyboard.":
        "贴图倍增 U 的值。提示：可用 PageDown 与 PageUp 键通过键盘调整数值。",
    "Texture multiplier V value": "贴图倍增 V 的值",
    "Textured with a check board": "使用棋盘格贴图",
    "Textured with a custom user image. Use 'Files->Load User Texture...' to load your texture.":
        "使用自定义用户图片贴图。通过「文件 → 载入自定义贴图...」载入纹理。",
    "Textured with a numerated grid. The grid texture can be changed persistently using the preference dialog (see Grid Texture).":
        "使用带编号的网格贴图。可通过首选项对话框持久更改网格贴图（见「网格贴图」）。",
    "The Auto Seams panel contains advanced algorithms to select automatically some edges of the visible islands set that would be good candidate to serve to cut and segment your islands.":
        "自动接缝面板包含若干高级算法，可自动在可见岛集合中选出适合用于切割与分割的边。",
    "The Edit Mode ToolBar contains selectors to change the principal RizomUV edition modes":
        "编辑模式工具栏包含用于切换 RizomUV 主要编辑模式的选择器。",
    "The Layout panel contains tools and settings related to island placement and areas in each UV tile. This panel is where you find tools such as Tools Pack, Fit and Rescale. As with Unwrap and Optimize, you can apply these settings on single, or multiple selections.":
        "布局面板包含与岛放置及每个 UV 贴图块区域相关的工具和设置，如排布、适配、重缩放等。与展开和优化一样，这些设置可作用于单个或多个选区。",
    "The Real Time Optimize engine move the vertexes around the point or edge or polygon selection set that you are currently transforming so that the distortion is minimized interactively. IMPORTANT: You will not have interesting result unless you add some pinning constraints on some vertexes before. It works by applying some optimize iterations on the islands in real time. Be carefully when dealing with dense meshes as this feature require heavy computation and it could slow down the viewport refresh rate.":
        "实时优化引擎会在你变换点/边/多边形选区时移动周围顶点，以交互方式最小化畸变。重要：如果事先没有在某些顶点上添加固定约束，效果不会明显。其原理是对岛实时执行若干次优化迭代。处理密集网格时请谨慎，此功能计算量大，可能降低视口刷新率。",
    "The classic projection panel contains basic tools to project your 3D geometry into flat UV coordinates.":
        "经典投影面板包含把 3D 几何体投影为平面 UV 坐标的基础工具。",
    "The color ID map editor allows you to define by island colors. To use it, switch to island selection mode (F4), then select some islands and apply some colors using the provided tools.":
        "颜色 ID 图编辑器可按岛定义颜色。使用方法：切换到岛选择模式（F4），选中若干岛后用提供的工具上色。",
    "The color map bar show relation between the viewport polygon's color and various numerical values.":
        "颜色图条显示视口多边形颜色与各种数值之间的对应关系。",
    "The debug command log file contains useful information that can be used to fix issues.":
        "调试命令日志文件包含可用于排查问题的信息。",
    "The distance used to propagate the transformation is the mesh based distance.":
        "用于传播变换的距离是基于网格的距离。",
    "The dynamic color palette shows currently used color among all the island set": "动态调色板显示当前所有岛中正在使用的颜色",
    "The empty space left on the UV tile's edge. As with a piece of printable paper, a UV map can have margins at the edges of the map.":
        "UV 贴图块边缘留出的空白。就像打印纸有页边距一样，UV 图也可以在边缘留边距。",
    "The horizontal resolution of the texture map. The value you set in this spinner-field affects Margin and Island Spacing, Room Space, some grid features, and some Distribute space features.":
        "贴图图的水平分辨率。此数值会影响边距与岛间距、空间余量、部分网格功能以及部分等距分布功能。",
    "The islands will not be pre-oriented before packing.": "排布前不会预先摆正岛。",
    "The minimal distance between where the island's borders intersect with themselves, in pixels or real (UV) units, depending on your Layout Panel's settings. WARNING, keep low values like 1 or 2 pixels maximum, otherwise you take the risk to block Optimize and Unfold features":
        "岛边界与自身相交处之间的最小距离，单位为像素或实际（UV）单位，取决于布局面板的设置。警告：请保持较低数值，最多 1 到 2 像素，否则可能导致优化与展开无法进行。",
    "The only things the channels will have in common are the geometry and 3D coordinates of the model when imported.":
        "各通道之间唯一共享的是导入时模型的几何体与 3D 坐标。",
    "The outline of the island/group determines placement while packing elements.": "排布元素时，岛/组的轮廓决定其放置方式。",
    "The outline of the island/group is replaced by a bounding- or control box while packing.":
        "排布时，岛/组的轮廓会被包围盒或控制盒替代。",
    "The path of the tile texture which is displayed when the texture mode is set to Texture Grid. Clear text to revert the built-in numeroted grid texture.":
        "当贴图模式设为「网格贴图」时所显示的贴图块纹理路径。清空文本可恢复内置的带编号网格贴图。",
    "The primitives will be crushed instead of being moved by groups.": "图元会被压缩，而不是按组整体移动。",
    "The proportional edition propagates the transformation applied to points/edges/polygons to a certain neighborhood.":
        "比例编辑会把施加在点/边/多边形上的变换传播到一定邻域。",
    "The protect/attract map will be used to determine the zones to protect from being selected. Red zones will prevents the edges to be selected.":
        "保护/吸引图用于确定需要保护、避免被选中的区域。红色区域会阻止边被选中。",
    "The range is determined automatically using the min and max texel density value on all islands":
        "范围根据所有岛上纹素密度的最小值和最大值自动确定。",
    "The slider controls the similarity parameters Rizom needs to process an island. If the slider is at 0, all topologically similar islands will be processed. Set to 1, Rizom will process islands of exact matching geometry. It's worth noting both topology and 3D coordinates (geometry) will be taken into consideration when Rizom compares islands for similarity under the hood.":
        "滑块控制 Rizom 处理岛时所需的相似度阈值。滑块为 0 时处理所有拓扑相似的岛；设为 1 时只处理几何完全一致的岛。请注意，Rizom 在内部比较相似度时会同时考虑拓扑与 3D 坐标（几何）。",
    "The spacing between the shells": "各个壳之间的间距",
    "The transform feature contains tools to translate, rotate, scale the selected points/edges/polygon/islands. It works by selecting some elements, then by doing one of this 3 actions:":
        "变换功能包含对选中的点/边/多边形/岛进行平移、旋转、缩放的工具。用法是先选中元素，再执行以下三种操作之一：",
    "Then click on the Selects icon if you just want to select edge or click on Flatten if you want the edges to be cut then new islands flattened, or on Pack if you a full auto unwrapping process including packing.":
        "如果只想选边，点击「选择」图标；如果希望沿边切割并展平新岛，点击「展平」；如果希望包含排布的全自动展开流程，点击「排布」。",
    "Then if you run a pack with nothing selected, the group itself will be transformed tightly like the other islands that are not inside a group and the other groups.":
        "此后在未选中任何内容的情况下执行排布，组本身会像其他不在组内的岛和其他组一样被紧密变换。",
    "Theses selection tools help you to select primitives or islands. Their availability depends on which mode you are in. Please note that some tools need a selection to work.":
        "这些选择工具可帮助你选择图元或岛。其可用性取决于当前所处模式。请注意，某些工具需要已有选区才能工作。",
    "This feature controls the multiple UV Tile layout. As it is sometimes more appropriate to place islands into several tiles instead of a single one, this feature gives the possibility to create a grid of UV tiles.":
        "此功能控制多 UV 贴图块布局。有时把岛放进多个贴图块比只放一个更合适，因此这里可以创建 UV 贴图块网格。",
    "This option is especially handy for complex, triangulated mesh. When active, it will try to find a straight selection of edges, creating a straight path where possible. It will do this even where a plethora of ngons are connected - which will not happen if this mode is disabled.":
        "此选项对复杂三角化网格尤为有用。启用后会尝试找出直线的边选择，尽可能生成笔直路径；即使那里连接了大量 n 边形也会如此，而禁用此模式则不会。",
    "This option will fit each selected island, or a selected and connected group of primitives rather than treating the entire selection as a single element.":
        "此选项会分别适配每个选中的岛，或每组选中且相连的图元，而不是把整个选区当作一个元素。",
    "This panel consists of tools specifically created to select sets of islands based on the parameters you define.":
        "此面板包含专门用于按你设定的参数选择岛集合的工具。",
    "This section is all about manual layouts and making them easier to work with, using tools created to straighten, align, flip, fit, and distribute. Tool usage is, of course, dependent on your current Primitive Selection Mode, but lot of them work in most modes.":
        "本节专注于手动布局，提供拉直、对齐、翻转、适配和分布等工具以便操作。工具的可用性取决于当前图元选择模式，但多数工具在大多数模式下都能用。",
    "This sets the selected UV Set from the channel list as current. You can also double click on the said list item to set it as current.":
        "将通道列表中选中的 UV 集设为当前。也可以双击该列表项来设为当前。",
    "Tile Border": "贴图块边框",
    "Tile ID Display mode": "贴图块编号显示模式",
    "Tile Size U": "贴图块尺寸 U",
    "Tile Size V": "贴图块尺寸 V",
    "Tile Texture File Browser": "浏览贴图块纹理文件",
    "Tip: Take a look at the Show Model Groups Dialog, it contains useful tools to help you select sub-parts of your model. You can choose Objects / Materials / Smoothing Groups / Groups if available in the imported file, as well as auto group and tile them.":
        "提示：可以看看「显示模型组」对话框，里面有帮助你选择模型子部件的有用工具。若导入文件包含对象/材质/平滑组/组信息，可以按这些分类选择，也可以自动分组与分块。",
    "To ungroup, press CTRL+G": "要取消分组，请按 CTRL+G",
    "TopoCopy": "拓扑复制",
    "Topology : Polygon color from vertex and edge and polygon count": "拓扑：多边形颜色取自顶点数、边数与多边形数量",
    "Transform Enable Rotation by angle increment": "变换：按角度增量旋转",
    "Transform Enable Scaling in U axis": "变换：启用 U 轴缩放",
    "Transform Enable Scaling in V axis": "变换：启用 V 轴缩放",
    "Transform Enable Translation in U axis": "变换：启用 U 轴平移",
    "Transform Enable Translation in V axis": "变换：启用 V 轴平移",
    "Transform Island Enable": "变换：启用岛",
    "Transform selected groups of edges so that they become parallel.": "变换选中的边组，使其相互平行。",
    "U & V": "U & V",
    "U Tiling Factor": "U 平铺系数",
    "UI background color": "界面背景色",
    "UI foreground color": "界面前景色",
    "UV Mapping Application": "UV 展开软件",
    "UV Multi-tile Column Count": "多 UV 贴图块列数",
    "UV Tile Reset": "重置 UV 贴图块",
    "UnGrow polygon/edge/point selection": "收缩多边形/边/点选择",
    "Unconstrain Edge(s) (Hotkey: Alt-Shift-C)": "取消约束边（快捷键：Alt-Shift-C）",
    "Unlink U and V Texture Tiling Factor.": "取消 U 与 V 贴图平铺系数的链接。",
    "Unpins selected point(s). Unpin all points if none selected. Can be also applied on island selection.":
        "取消固定选中的点；若未选中则取消固定所有点。也可作用于选中的岛。",
    "Update unwrap mode after a cut or a weld action. Choose Disabled option for heavy as since it can slow down the responsiveness":
        "切割或焊接后更新展开模式。资产较重时建议选择「禁用」，因为它可能降低响应速度。",
    "Updates the seams and the UV coordinates of the similar islands provided that their similarity matches. It's worth noting that this is not the same as the Stack Similar function, as Update Similar as it left the islands at their current location rather than forming a stack.":
        "在相似度符合条件时，更新相似岛的接缝与 UV 坐标。注意这与「堆叠相似岛」不同：更新相似岛会保持岛在原位置，而不是形成堆叠。",
    "Use Custom Texel Density": "使用自定义纹素密度",
    "Use a center specified by text entries for scaling and rotating.": "使用数值输入框指定的中心进行缩放与旋转。",
    "Use a center specified by the mouse pointer for scaling and rotating.": "使用鼠标指针指定的中心进行缩放与旋转。",
    "Use a per primitive group or per island center for scaling and rotating.": "按每个图元组或每个岛的中心进行缩放与旋转。",
    "Use absolute uv space distance to determine the snapping distance": "使用 UV 空间的绝对距离来确定吸附距离",
    "Use custom texel density value instead of the layout panel's one.": "使用自定义纹素密度值，而非布局面板中的值。",
    "Use in edge, polygon mode to create seams on the mesh. If the selection is empty, the edge located under the mouse pointer will be cut.":
        "在边、多边形模式下用于在网格上创建接缝。若没有选区，则切割鼠标指针下的边。",
    "Use the bounding box's center for scaling and rotating.": "使用包围盒中心进行缩放与旋转。",
    "Use the grid size to determine the snapping distance.": "使用网格尺寸来确定吸附距离。",
    "Use the minimal bounding box's axis for the transformation": "使用最小包围盒的轴向进行变换",
    "Use world's axis for the transformation.": "使用世界轴向进行变换。",
    "Using 'Cut' means the current UV space topology is used.": "使用「切割」表示采用当前 UV 空间的拓扑。",
    "Using 'Uncut' means that the original loaded topology in 3D space is used.": "使用「未切割」表示采用 3D 空间中原始载入的拓扑。",
    "Using Both will enable Rizom to process islands which have the same topology and normal orientation, as well as symmetrically identical islands which are inverted.":
        "使用「两者」会让 Rizom 同时处理拓扑与法线朝向相同的岛，以及法线翻转的对称相同岛。",
    "Using Straight mode will enable Rizom to process geometrically identical islands with the same normal orientation only.":
        "使用「直向」模式时，Rizom 只处理几何相同且法线朝向相同的岛。",
    "Using TopoCopy": "使用拓扑复制",
    "Using the Pick Density eyedropper picks the Texel Density from the currently selected island(s). If none are selected, Rizom calculates the average Texel Density of all presently visible islands. You can also set your Texel Density manually in the spinner-field next to the eyedropper.":
        "用「拾取密度」吸管可从当前选中的岛读取纹素密度。若未选中任何岛，Rizom 会计算所有当前可见岛的平均纹素密度。也可以在吸管旁的数值框中手动设定纹素密度。",
    "Usual UV layouts use UV tiles shaped like an unity square (1x1), with the tile low left corner placed at origin.":
        "常见的 UV 布局使用 1×1 的方形 UV 贴图块，贴图块左下角位于原点。",
    "V Tiling Factor": "V 平铺系数",
    "Value is not the same for all islands/groups of the current selection.": "当前选区内的岛/组取值并不相同。",
    "Value not set, so it pick up the settings defined via Global.": "未设定值，因此沿用「全局」中的设置。",
    "Very high number of cuts, very low distortion": "极多切割，极低畸变",
    "Viewport far plane distance from camera": "视口远裁剪面到相机的距离",
    "Weld Magnet Distance": "焊接磁吸距离",
    "Weld edges that can be welded without creating overlaps. WARNING: If enabled, the stretch limit and angle limit may not be respected and may create additional distortion.":
        "焊接可以焊合且不会产生重叠的边。警告：启用后可能无法遵守拉伸与角度限制，并产生额外畸变。",
    "Welds selected edges, polygons, or islands. If the selection is empty, the edge or loop located under the mouse pointer, if any, will be welded.":
        "焊接选中的边、多边形或岛。若没有选区，则焊接鼠标指针下的边或边循环（如果有）。",
    "What is Topology?": "什么是拓扑？",
    "When active, Unfold and Optimize avoid creation of self border intersections. PLEASE NOTE: This can significantly increase the unwrapping or optimizing calculation time.":
        "启用后，展开与优化会避免边界自相交。请注意：这可能显著增加展开或优化的计算时间。",
    "When active, Unfold and Optimize will not block the vertexes that are on the selection set limit so that they can freely move.":
        "启用后，展开与优化不会固定选区边界上的顶点，使其可以自由移动。",
    "When enabled, the selection will be visible behind the polygons": "启用后，选中项在多边形后方也可见",
    "When enabled, the selection will behave like a rubber. Else it will behave like a modeling clay. In other terms, if enabled, the island's deformation will be reseted to its initial unfolded shape before being conformed to user's constrains.":
        "启用后，选区行为像橡皮；否则像塑形黏土。换言之，启用时会先把岛变形重置为初始展开形状，再按用户约束贴合。",
    "When set to active, running Unfold and Optimize avoid the creation of triangle flips. PLEASE NOTE: This can significantly increase the unwrapping or optimizing calculation time.":
        "启用后，执行展开与优化时会避免产生三角形翻转。请注意：这可能显著增加展开或优化的计算时间。",
    "When using the check board as a texture map, it is preferable to set values superior to 1. The more your mesh will contains smaller parts, the more greater values will be generally appropriate to see correctly the distortion.":
        "使用棋盘格作为贴图时，建议把数值设为大于 1。网格包含的小部件越多，通常越需要更大的数值才能正确观察畸变。",
    "Will invert the current map (on selected islands, or all islands if none selected)": "反转当前贴图（作用于选中的岛；若未选中则作用于全部岛）",
    "Will set the current map to his neutral value (on selected islands, or all islands if none selected)":
        "把当前贴图设为中性值（作用于选中的岛；若未选中则作用于全部岛）",
    "Works only if the mesh is perfectly symmetric (both the topology and 3D vertexes position must be symmetrical). Under your 3D software at modeling stage, use appropriate tools to force the geometry to be symmetric. Then use the smallest point tolerance possible that allows symmetry.":
        "仅当网格完全对称时有效（拓扑与 3D 顶点位置都必须对称）。请先在 3D 软件的建模阶段用合适的工具强制几何体对称，然后使用能识别对称的最小点容差。",
    "Worth noting that only edges that have been previously cut can be welded.": "注意，只有之前被切割过的边才能被焊接。",
    "Write Command Log Into File": "将命令日志写入文件",
    "Write OpenGL Debug Into File": "将 OpenGL 调试信息写入文件",
    "Write command log into file (for debugging purpose)": "将命令日志写入文件（用于调试）",
    "Write openGL debug message into file (for debugging purpose)": "将 OpenGL 调试信息写入文件（用于调试）",
    "You activate the edge loop feature by double - clicking on an edge in your topology.":
        "在拓扑中双击一条边即可启用边循环功能。",
    "You start Packing by pressing P on your keyboard. You use the packing panel to define all the settings which come into play when the packing algorithm packs your visible islands or groups. Once you've set these, the algorithm will then proceed to pack with the parameters you defined.":
        "按 P 键即可开始排布。排布面板用于设定排布算法处理可见岛或组时的各项参数，设定完成后算法会按你定义的参数执行排布。",
    "Your favorite text and script editor program path.": "你常用的文本与脚本编辑器程序路径。",
    "and 3D vertexes position must be symmetrical). Under your 3D software at modeling stage, use appropriate tools to force the geometry to be symmetric. Then use the smallest point tolerance possible that allows symmetry.":
        "且 3D 顶点位置必须对称）。请先在 3D 软件的建模阶段用合适的工具强制几何体对称，然后使用能识别对称的最小点容差。",

    # ------------------------------------------------------------ 短标签与选项
    "B.Box Center": "包围盒中心",
    "Auto Select Box will select the edge intersecting virtual box faces X+ and Y+": "自动选择盒式会选中与虚拟盒 X+ 和 Y+ 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X+ and Y-": "自动选择盒式会选中与虚拟盒 X+ 和 Y- 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X+ and Z+": "自动选择盒式会选中与虚拟盒 X+ 和 Z+ 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X+ and Z-": "自动选择盒式会选中与虚拟盒 X+ 和 Z- 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X- and Y+": "自动选择盒式会选中与虚拟盒 X- 和 Y+ 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X- and Y-": "自动选择盒式会选中与虚拟盒 X- 和 Y- 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X- and Z+": "自动选择盒式会选中与虚拟盒 X- 和 Z+ 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces X- and Z-": "自动选择盒式会选中与虚拟盒 X- 和 Z- 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces Y+ and Z+": "自动选择盒式会选中与虚拟盒 Y+ 和 Z+ 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces Y+ and Z-": "自动选择盒式会选中与虚拟盒 Y+ 和 Z- 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces Y- and Z+": "自动选择盒式会选中与虚拟盒 Y- 和 Z+ 面相交的边",
    "Auto Select Box will select the edge intersecting virtual box faces Y- and Z-": "自动选择盒式会选中与虚拟盒 Y- 和 Z- 面相交的边",
    "Box Mode": "盒式模式",
    "Classic Projection": "经典投影",
    "Constrain Edge(s) Aligned": "约束边对齐",
    "Constrain Edge(s) Horizontally": "约束边水平",
    "Constrain Edge(s) Vertically": "约束边垂直",
    "Details Remover": "细节移除",
    "Display Both": "显示两者",
    "Display Flats": "显示已展平",
    "Display Not Flats": "显示未展平",
    "Edge Loop": "边循环",
    "Fit to Pixel": "适配到像素",
    "Island Groups Panel": "岛组面板",
    "Island Stretch": "岛拉伸",
    "Max Deviation Normal": "最大偏差法线",
    "Max Edge Angle": "最大边角度",
    "Max Mutations": "最大变异次数",
    "Pick Density (Hotkey: Alt-Q)": "拾取密度（快捷键：Alt-Q）",
    "Proportional Edit": "比例编辑",
    "Set Density Uniformly": "统一设置密度",
    "Show Island Group Outlines": "显示岛组轮廓",
    "Show Island Group BBoxes": "显示岛组包围盒",
    "Show Island Group Labels": "显示岛组标签",
    "Snap Distance Mode": "吸附距离模式",
    "Stack Symmetrical": "对称堆叠",
    "Texture Tiling Ratio": "贴图平铺比例",
    "Tile Margin": "贴图块边距",
    "UV Tiles": "UV 贴图块",
    "Update Unwrap": "更新展开",
    "Use Absolute Distance": "使用绝对距离",
    "Use Grid Size": "使用网格尺寸",

    # ------------------------------------------------------------ 第二批补充
    "Enable Grid Visibility": "启用网格可见",
    "Enable grid snap.": "启用网格吸附。",
    "Enable grid visibility.": "启用网格可见。",
    "Enable point snapping on island vertexes borders.": "启用岛顶点边界上的点吸附。",
    "Enable/Disable Scaling in V axis.": "启用/禁用 V 轴缩放。",
    "Enable/Disable Translation in U axis.": "启用/禁用 U 轴平移。",
    "Enable/Disable Translation in V axis.": "启用/禁用 V 轴平移。",
    "Enable/Disable rotation by angle increment.": "启用/禁用按角度增量旋转。",
    "Enable/Disable scaling in U axis.": "启用/禁用 U 轴缩放。",
    "If enabled, Unfold and Optimize features stops when the distortion energy becomes sufficiently low or stagnates. If disabled, Unfold and Optimize stop when the specified Iteration Count is reached. It's worth noting that if you're not sure about your iterations, you should turn this back on, as it's the better in 99% of unwrapping cases. If you are dealing with dense geometry and the Auto mode takes ages to compute, or inversely does nothing, use the spinners of the manual mode.":
        "启用后，当畸变能量足够低或趋于停滞时，展开与优化会提前停止。禁用后，展开与优化会在达到指定迭代次数时停止。请注意：如果不确定迭代次数，建议保持开启，因为在 99% 的展开场景下这样效果更好。若处理密集几何体时自动模式耗时极长或几乎没有效果，可改用手动模式的数值框。",
    "Packing algorithm accuracy. \t\tPut higher settings only in presence of very small islands only.":
        "排布算法精度。仅在存在极小岛时才建议提高此设置。",
    "Pick relative texel density of the current island selection and set it for next packing operations. WARNING: if the 'Auto fit' option is enabled, the whole tile will be rescaled, so that you the specified texel density will not be kept.":
        "拾取当前选中岛的相对纹素密度，用于后续排布操作。警告：若启用了「自动适配」，整个贴图块都会被重新缩放，指定的纹素密度将无法保持。",
    "Please note that each tile, island group(s), and single islands can have custom settings. To change their parameters, select the ones you want to customize, and then change their values. The new, custom values will override the default or previously set values of their island group or tile. If you want to remove specific parameters on a particular element (tile / island group / island), select the item(s), then press CTRL + G or the 'Global' button.":
        "请注意，每个贴图块、岛组和单个岛都可以有自定义设置。要修改参数，先选中要自定义的对象，再修改其数值。新的自定义值会覆盖其所属岛组或贴图块的默认值或先前设定值。若要移除某个对象（贴图块/岛组/岛）上的特定参数，选中该对象后按 CTRL + G 或点击「全局」按钮。",
    "Preferences FBX 2010": "首选项 FBX 2010",
    "Preferences FBX 2011": "首选项 FBX 2011",
    "Preferences FBX 2012": "首选项 FBX 2012",
    "Preferences FBX 2013": "首选项 FBX 2013",
    "Preferences FBX 2014/2015": "首选项 FBX 2014/2015",
    "Preferences FBX 2016": "首选项 FBX 2016",
    "Preferences FBX 2018": "首选项 FBX 2018",
    "Preferences File Name Suffix": "首选项 文件名后缀",
    "Preferences Recent file list open 3D instead of UVs": "首选项 最近文件列表以 3D 模式打开",
    "Preferences Reset All Settings": "首选项 重置所有设置",
    "Preferences Undo History Size": "首选项 撤销历史步数",
    "RizomUV is capable of handling several UV channels and allows you to have several channels, i.e. for light-baking, with different layouts and cuts.":
        "RizomUV 支持多个 UV 通道，例如用于烘焙光照的通道，可以拥有不同的布局与切割。",
    "Select some edges then hit key 'C' for cut and 'W' for weld/uncut them. Then hit 'U' to unfold your mesh. When something is selected, hit 'TAB' to display the Gizmo and have a rapid access to rotate, translate and scale. Press key 'D' + mouse buttons to drag the island located under the mouse pointer.":
        "选中一些边后按 C 切割、按 W 焊接/取消切割，然后按 U 展开网格。有选区时按 TAB 可显示操纵器，快速旋转、平移和缩放。按住 D 键加鼠标键可拖动鼠标指针下的岛。",
    "Select which topology the similar island tools will use to compare the processed geometry.":
        "选择相似岛工具比较处理过的几何体时所使用的拓扑。",
    "Switch to edit mode density multiplier map. Once edited, a value of the density multiplier different from zero will change the UV polygon's area after running optimize.":
        "切换到密度倍增图编辑模式。编辑后，非零的密度倍增系数会在执行优化后改变 UV 多边形的面积。",
    "TIP: If you don't select islands that are inside a group, thoses islands will not be transformed **unless** the Pack All option is down. If Pack All is down, all element inside groups will be repacked, excepted for the groups that are in Stack mode (see below this special case).":
        "提示：如果未选中组内的岛，这些岛不会被变换，**除非**按下了「排布全部」。按下「排布全部」时，组内所有元素都会被重新排布，但处于堆叠模式的组除外（见下方特殊说明）。",
    "TIP: In primitive edge selection mode, this dialog will select the polygon set's frontiers, not the edges that are included in them.":
        "提示：在图元边选择模式下，此对话框会选中多边形集合的边界，而不是集合内部的边。",
    "Target relative texel density for next packing operations. WARNING: if the 'Auto fit' option is enabled, the whole tile will be rescaled, so that you the specified texel density will not be kept.":
        "后续排布操作的目标相对纹素密度。警告：若启用了「自动适配」，整个贴图块都会被重新缩放，指定的纹素密度将无法保持。",
    "The grid serves as a guide to place your element in UV spaces. Enable Snap to male points/edges/polygon/island by snapped to the grid when transforming them.":
        "网格可作为在 UV 空间中放置元素的参考。启用吸附后，变换时点/边/多边形/岛会吸附到网格。",
    "When active, Unfold and Optimize fill the mesh's holes by adding invisible, temporary polygons to the model, so when an unwrap or optimize occurs, it prevents the hole from collapsing on various types of unwraps. Use this on eyes, mouths, nostrils, clothing and hard edge openings like the hole on top of a tank or non-square windows.":
        "启用后，展开与优化会向模型添加不可见的临时多边形来填补网格孔洞，从而在展开或优化时避免孔洞塌陷。适用于眼睛、嘴、鼻孔、衣物，以及罐体顶部开孔、非方形窗洞等硬边开口。",
    "You can also define the behavior of the Edge Loop Selection when working in Edge Mode : You can set it to find the shortest path between two edges in opposite ends using the V - key.Or switch back to edge loop selection using the B key.":
        "在边模式下还可以定义边循环选择的行为：可用 V 键改为在两端之间寻找最短路径，或用 B 键切回边循环选择。",
    "Selected: 0 | Hidden: 0 | Total: 0": "已选中: 0 | 已隐藏: 0 | 总计: 0",

    # ------------------------------------------------------------ 第三批：帮助面板长文与许可证界面
    "Texture Multipliers are two factors that affect the current texture map viewport rendering size in the U and V direction. Hit PageUp and PageDown keys to change the texture multipliers. If the factors are both equal to 1, the texture map will be mapped one time in the UV tile. If the factor are augmented, the texture map will be repeated the number or time it is specified by the value in U and V direction.":
        "贴图倍数是两个系数，影响当前贴图在视口中 U、V 方向的显示尺寸。按 PageUp 与 PageDown 键可调整贴图倍增。两个系数都为 1 时，贴图在 UV 贴图块中只映射一次；系数增大后，贴图会按 U、V 方向的数值重复相应次数。",
    "This panel defines how you want the Edge Loop tool to behave, it will appear when you select working in Edge mode by clicking the icon, the menu or using the F2 key.":
        "此面板定义边循环工具的行为方式。当你通过点击图标、菜单或按 F2 键进入边模式工作时，面板会出现。",
    "When it comes to 3D, topology means the layout of the polygons which compose the mesh.By layout, we mean how polygons and /or the edges that make up the model's shape are connected to each other.Topology can affect a lot of things in a 3D workflow, not just UV maps, such as ease of texturing or modifying the model's shape.When you use a UV mapping application, you use the edges in the mesh to cut and adjust your UV map, so it's as flat as possible for texturing.Good topology, meaning an even distribution of quads in the model makes it significantly easier to work with before i.e a game engine triangulates it.It will give cleaner triangles at that point as well.":
        "在 3D 领域，拓扑指构成网格的多边形的排布方式。「排布」指构成模型形状的多边形和/或边之间的连接关系。拓扑会影响 3D 工作流中的许多环节，不只是 UV 图，还包括贴图难易度、模型形状修改等。使用 UV 展开软件时，你会利用网格中的边来切割并调整 UV 图，使其尽可能平整以便贴图。良好的拓扑意味着模型中四边形分布均匀，这在游戏引擎进行三角化之前能显著降低处理难度，三角化后也能得到更干净的三角形。",
    "Whether you cut and unwrap as you go, or do all your cuts and then unwrap, at some point you are going to need to use the Unwrap panel. To use it, your island(s) need at least one UV- or hard seam. (a hard seam is a cut in your model, not your UVs). Once you hit U to unwrap, RizomUV calculates the flattest and most distortion-less unwrap possible. There are several ways you can press the U key to unwrap: Either press U to unwrap all visible and non-flat islands, or select some primitives then hit U, or mouse-over an island and hit U. Once flattened, you can run an Optimize via the O key, to get rid of even more distortion. Using Optimize follows the same rules as the U-key. Get to know the Unwrap panel and its shortcuts for fast and flat unwraps.":
        "无论是边切边展，还是先切完再统一展开，最终都会用到展开面板。使用时，岛至少需要一条 UV 接缝或硬接缝（硬接缝指模型上的切割，而不是 UV 上的）。按 U 展开时，RizomUV 会计算出尽可能平整、畸变尽可能小的展开结果。按 U 展开有几种方式：直接按 U 展开所有可见且未展平的岛；先选中一些图元再按 U；或把鼠标悬停在某个岛上再按 U。展平后可按 O 执行优化，进一步消除畸变。优化的作用规则与 U 键相同。熟悉展开面板及其快捷键，可以让展开又快又平整。",
    "The TopoCopy toolset was created to make it even easier to work with similar islands in your mesh. Because TopoCopy targets similar elements in your model, even if they are geometrically, but not topologically different, you can now truly copy cuts and unwraps from one island to another, including topology that had pinch or spread fixed, or was just in need of a little tender love and optimizing. Your main starter tool in this panel is the Similarity slider.You can use the Similarity slider to define how similar, or not, your islands or elements need to be for your updated topology to be copied over to them.":
        "拓扑复制工具集旨在让处理网格中的相似岛更轻松。由于拓扑复制针对的是模型中的相似元素——即使它们在几何上不同但拓扑相同——现在你真正可以把切割与展开结果从一个岛复制到另一个岛，包括经过收缩/扩散修整的拓扑，或只是需要一点细致优化的拓扑。此面板中最主要的入门工具是「相似度」滑块，用它定义岛或元素需要多相似，更新后的拓扑才会被复制过去。",
    "Available mode distributes evenly the available space between selected items. Real mode distributes the specified space in real unit between items. Pixel mode distributes the specified space in pixel unit between items.":
        "「可用」模式会把可用空间在选中项目之间均匀分配。「实际」模式按实际单位在项目之间分配指定间距。「像素」模式按像素单位在项目之间分配指定间距。",
    "3. Changing directly the values in the controllers (you can multiply/divide/add/subtract current values by others, mathematic expressions are interpreted).":
        "3. 直接修改输入框中的数值（可用其他值对当前值做乘/除/加/减，支持数学表达式）。",
    "Cut island in two if its maximum bounding box length over the average of the maximum bounding box length of all islands exceeds the LengthRatio.":
        "当岛的最大包围盒长度与所有岛最大包围盒长度平均值之比超过「长度比例」时，将该岛切成两半。",
    "Enable Max Relative Angle to select revolution or curved shapes. The more the angle is high, the more you will select polygons. Try small values before and augment the value until you get enough selected polygons.":
        "启用「最大相对角度」以选择旋转体或曲面形状。角度越大，选中的多边形越多。建议先从小值开始，逐步加大直到选到足够的多边形。",
    "Isolate selected islands or the island under the mouse. If nothing is selected, this will make visible all islands, excluding the ones that have been hidden using \"Hide Selected\".":
        "孤立选中的岛或鼠标下的岛。若没有选中任何内容，则显示所有岛，但通过「隐藏选中」隐藏的岛除外。",
    "Select edges using the Hierarchical Pelt algorithm. Extremities of the visible islands will be linked (if Pelt is activated) and the hierarchy sections will be also selected if Trunk/Branches/Leafs are enabled.":
        "使用层级剥皮算法选边。可见岛的末端会被连接（若启用了剥皮），且当主干/枝干/叶片选项启用时，层级分段也会被选中。",
    "Select Mosaic when dealing with big terrains or hard surface models or mesh coming from photogrammetry. If you deal with CAD model that contains some revolution shapes, \"Fit Cones\" can help to produce better segmentation.":
        "处理大型地形、硬表面模型或摄影测量网格时，请选择「马赛克」。若处理含旋转体形状的 CAD 模型，「适配圆锥」有助于获得更好的分割效果。",
    "Value near 1 will make the mesh's small details ignored. Warning: Too much denoise can make some local stretching appears, even if the stretch limiter is enabled.":
        "数值接近 1 时会忽略网格的细小细节。警告：去噪过度可能导致局部出现拉伸，即使启用了拉伸限制也一样。",
    "PLEASE NOTE: if AutoFit is enabled, the island will be rescaled after packing finishes.":
        "请注意：若启用了「自动适配」，排布完成后岛会被重新缩放。",
    "Use the viewport zoom to determine the snapping distance.": "使用视口缩放来确定吸附距离。",
    "UV viewport background color": "UV 视口背景色",
    "Show Advanced Options": "显示高级选项",
    "Switch to edit mode brush optimize": "切换到笔刷优化编辑模式",
    "Switch to edit mode brush unfold": "切换到笔刷展开编辑模式",
    "Pin Map Enable": "固定图启用",
    "Transform Center U": "变换中心 U",
    "Transform Center V": "变换中心 V",
    "Transform Rotate Inc W": "变换旋转增量 W",
    "Transform Rotate W": "变换旋转 W",
    "Transform Scale U": "变换缩放 U",
    "Transform Scale V": "变换缩放 V",
    "Transform Translate U": "变换平移 U",
    "Transform Translate V": "变换平移 V",
    "CHANGE LICENSE FILE...": "更改许可文件...",
    "OR RESET SERVER LOCATION": "或重置服务器位置",
    "PERPETUAL LICENSE INFORMATION": "永久许可信息",
    "SHOW THIS LICENSE IN RIZOM-LAB ACCOUNT": "在 RIZOM-LAB 账户中查看此许可",
    "THIS COMPUTER HOST ID": "本机主机 ID",
    "Email account:": "邮箱账户：",
    "Expiration Date:": "到期日期：",
    "Padding": "边距填充",
    "Profile": "配置",
    "Area Tool Mode Circle": "区域工具：圆形",
    "Edge Loop Path Iteration": "边循环路径迭代次数",
    "UV Channel ()": "UV 通道 ()",
    "Launch registered LUA script files (.lua)": "运行已注册的 LUA 脚本文件（.lua）",
    "Select polygon set using geometric characteristics.": "按几何特征选择多边形集合。",
}
