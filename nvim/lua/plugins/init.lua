return {
	{
		'nvim-telescope/telescope.nvim', tag = 'master',
		dependencies = { 'nvim-lua/plenary.nvim' }
	},
	{
		'sainnhe/sonokai',
		lazy = false,
		priority = 1000,
		config = function()
			-- Optionally configure and load the colorscheme
		vim.g.sonokai_enable_italic = true
			vim.cmd.colorscheme('sonokai')
		end
	},
	{
		'nvim-treesitter/nvim-treesitter',
		lazy = false,
		branch = 'main',
		build = ':TSUpdate',
		config = function() 
			local ensure_installed = {
				"arduino","asm","bash","c","c_sharp","cairo","cpp","css",
				"csv","desktop","gdscript","html","kdl","latex","lua","make",
				"markdown","matlab","python","r","rust","scss","toml","vim"
			}

			require'nvim-treesitter'.install(ensure_installed)
			local filetypes = {}
			for lang = 1,#ensure_installed,1 do

				local files = vim.treesitter.language.get_filetypes(ensure_installed[lang])
				for i=1,#files do
					filetypes[#filetypes+1] = files[i]
				end
			end
			vim.api.nvim_create_autocmd({ 'Filetype' }, {
				pattern = filetypes,
				callback = function()
					vim.wo.foldexpr = 'v:lua.vim.treesitter.foldexpr()'
					vim.bo.indentexpr = "v:lua.require'nvim-treesitter'.indentexpr()"
					vim.treesitter.start()
				end
			})
		end
	},
	{
	    'MeanderingProgrammer/render-markdown.nvim',
	    dependencies = { 'nvim-treesitter/nvim-treesitter', 'nvim-mini/mini.nvim' },
	    opts = {}
	},
	{
	  {
	    "nvim-neo-tree/neo-tree.nvim",
	    branch = "v3.x",
	    dependencies = {
	      "nvim-lua/plenary.nvim",
	      "MunifTanjim/nui.nvim",
	      "nvim-tree/nvim-web-devicons", -- optional, but recommended
	    },
	    lazy = false, -- neo-tree will lazily load itself
	  }
	},
	{
		"nvim-telescope/telescope-file-browser.nvim",
		dependencies = { "nvim-telescope/telescope.nvim", "nvim-lua/plenary.nvim" },
		config = function() 
			require("telescope").setup {
				theme = "ivy",
		        	hijack_netrw = true,
			}
			require("telescope").load_extension("file_browser")
		end
	},
	{

		"mbbill/undotree"
	},
	{

		"tpope/vim-fugitive"
	},

	{
		"neovim/nvim-lspconfig"
	},
	{
		"Saghen/blink.cmp",
		dependencies = { 'rafamadriz/friendly-snippets' },
        tag = "v1.7.0",
		---@module 'blink.cmp'
		---@type blink.cmp.Config
		opts = {
		    -- 'default' (recommended) for mappings similar to built-in completions (C-y to accept)
		    -- 'super-tab' for mappings similar to vscode (tab to accept)
		    -- 'enter' for enter to accept
		    -- 'none' for no mappings
		    --
		    -- All presets have the following mappings:
		    -- C-space: Open menu or open docs if already open
		    -- C-n/C-p or Up/Down: Select next/previous item
		    -- C-e: Hide menu
		    -- C-k: Toggle signature help (if signature.enabled = true)
		    --
		    -- See :h blink-cmp-config-keymap for defining your own keymap
		    keymap = { preset = 'default' },

		    appearance = {
		      -- 'mono' (default) for 'Nerd Font Mono' or 'normal' for 'Nerd Font'
		      -- Adjusts spacing to ensure icons are aligned
		      nerd_font_variant = 'mono'
		    },

		    -- (Default) Only show the documentation popup when manually triggered
		    completion = { documentation = { auto_show = false } },

		    -- Default list of enabled providers defined so that you can extend it
		    -- elsewhere in your config, without redefining it, due to `opts_extend`
		    sources = {
		      default = { 'lsp', 'path', 'snippets', 'buffer' },
		    },

		    -- (Default) Rust fuzzy matcher for typo resistance and significantly better performance
		    -- You may use a lua implementation instead by using `implementation = "lua"` or fallback to the lua implementation,
		    -- when the Rust fuzzy matcher is not available, by using `implementation = "prefer_rust"`
		    --
		    -- See the fuzzy documentation for more information
		    fuzzy = { implementation = "rust" }
		  },
		  opts_extend = { "sources.default" }
	}
}
