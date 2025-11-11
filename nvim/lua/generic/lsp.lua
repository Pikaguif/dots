vim.lsp.enable('ruff')
vim.lsp.enable('ccls')
vim.lsp.enable('lua_ls')
vim.lsp.enable('rust_analyzer')
vim.lsp.enable('html')
vim.lsp.enable('ltex-plus')
vim.lsp.config('ltex-plus', {
    settings = {
        language = "auto"
    }
})
