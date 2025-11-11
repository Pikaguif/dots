vim.opt.ambw = "single"
vim.opt.autoindent = true

vim.opt.breakindent = true
vim.opt.breakindentopt = "shift:-2"

	-- This is an example for a multiline commnet, I want to see how well it works the breakindnt thingy because if it realy does look good we might keep it

vim.opt.nu = true
vim.opt.relativenumber = true

vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true

vim.opt.smartindent = true

vim.opt.backup = false
vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir"
vim.opt.undofile = true


vim.opt.scrolloff = 6
vim.opt.signcolumn = "yes"

vim.opt.isfname:append("@-@")

vim.opt.colorcolumn = "80"
