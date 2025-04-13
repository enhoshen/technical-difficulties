# Tracing lua code as a begginer

<!--toc:start-->

- [Tracing lua code as a begginer](#tracing-lua-code-as-a-begginer)
  - [Understanding keymapping in `Snacks.picker`](#understanding-keymapping-in-snackspicker)
  <!--toc:end-->

## Understanding keymapping in `Snacks.picker`

So by default when using the neovim plugin `Snacks.picker`, there are a couple of keymaps such
as "toggle_hidden",

```lua
-- in snacks.picker.config.defaults
  win = {
    input = {
      keys = {
        -- to close the picker on ESC instead of going to normal mode,
        -- add the following keymap to your config
        -- ["<Esc>"] = { "close", mode = { "n", "i" } },
        ["/"] = "toggle_focus",
        ...
        ["<a-f>"] = { "toggle_follow", mode = { "i", "n" } },
        ["<a-h>"] = { "toggle_hidden", mode = { "i", "n" } },
```

I wanted to know want the key maps are actually mapped to, so immedately i go
for `grep toggle_hidden` under the `snacks` project and the only things come
up are these keymaps.

So I tried to find definition on `win` (lsp needed), it leads me to the class
`snacks.picker.win.Config`.
Also, when using the keymaps, when can do `:verbose map <a-f>`, it shows:

```
n  <M-h>       *@<Lua 811: ~/.local/share/nvim/lazy/snacks.nvim/lua/snacks/win.lua:334>
  toggle_hidden
Last set from Lua (run Nvim with -V1 for more details)
```

By the actions above I finally pinpoint where the keymaps are actually mapped.

Heading over to `snacks.win.lua:334`, I now know that `win.action` is what I was
looking for:

```lua
function M:action(actions)
  actions = type(actions) == "string" and { actions } or actions
  ---@cast actions string[]
  local desc = {} ---@type string[]
  for a, name in ipairs(actions) do
    desc[a] = name:gsub("_", " ")
    if self.opts.actions and self.opts.actions[name] then
      local action = self.opts.actions[name]
      desc[a] = type(action) == "table" and action.desc and action.desc or desc[a]
    end
  end
  return function()
    for _, name in ipairs(actions) do
      if self.opts.actions and self.opts.actions[name] then
        local a = self.opts.actions[name]
        local fn = type(a) == "function" and a or a.action
        local ret = fn(self)
        if ret then
          return type(ret) == "string" and ret or nil
        end
      elseif self[name] then
        self[name](self)
        return
      else
        return name
      end
    end
  end,
    table.concat(desc, ", ")
end
```

Without debugger, I used `vim.print()` all over the place and found out it will
not work great with tables. But at least I now know that items in
`self.opts.actions` are the mapping targets. At the same time I stumble across
a `Snacks.picker` keymap `<a-d>`, mapping to "inspect"

```lua
        ["<a-d>"] = { "inspect", mode = { "n", "i" } },
```

And in `snacks.picker.actions.lua` I can find the actual implementation `M.inspect`

```lua
--- inSnacks.picker.actions.lua
function M.inspect(picker, item)
  Snacks.debug.inspect(item)
end
```

So now we know the key is mapped to the item in the table `self.opts.actions`,
but `toggle_*` is no where to be found in the `snacks.picker.actions` module.
Weird...

As mentioned, `vim.print` doesn't work great with tables, so let's just call
`Snacks.debug.inspect(self.opts.actions)` in place of `vim.print`. Now when pressing the keyboard,
there will be a pop-up debug windows, and now I finally see there ARE action
items mapped to entries starting with "toggle\_"...

```lua
--- in the debug window
      toggle_hidden = {
        action = <function 42>,
        desc = "toggle_hidden",
        name = "toggle_hidden"
      },
```

Now I was really close, I need to know how actions are set in **run time**. I could
reason that somewhere a function with an input option such as `hidden` will be
appended by `toggle_` as the name and description, so I did `grep toggle_` one
last time in the snacks project and there we have the entry

```
config/init.lua|98 col 19| opts.actions["toggle_" .. name] = function(picker)`
```

Now I finally located where `toggle_*` are actually mapped, and what they are
actually mapped to...

```lua
  -- add hl groups and actions for toggles
  opts.actions = opts.actions or {}
  for name in pairs(opts.toggles) do
    local hl = table.concat(vim.tbl_map(function(a)
      return a:sub(1, 1):upper() .. a:sub(2)
    end, vim.split(name, "_")))
    Snacks.util.set_hl({ [hl] = "SnacksPickerToggle" }, { default = true, prefix = "SnacksPickerToggle" })
    opts.actions["toggle_" .. name] = function(picker)
      picker.opts[name] = not picker.opts[name]
      picker.list:set_target()
      picker:find()
    end
  end
```

Take home ideas:

- Use `Snacks.debug.inspect` for printing, before I takes the time to learn debugger
  for lua. Not sure if luadebugger would work well with nvim, since I use nvim dap
  to work with the debugger...
- Something as simple as this caused me so much trouble boggles me. Tracing code
  in a language that I am not really familiar with can be quite challenging for me,
  but seems like a good exercise to know more about the language.
- Look for `init.lua` for a module. I trace code from the bottom up, and finally
  get to the top initialize script for the `snacks.config` module. Tracing the
  code top down gives us thegreater picture quickly.
