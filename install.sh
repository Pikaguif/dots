#! /bin/sh

# Work in progress

cp ./niri ~/.config/niri
cp ./hyprlock ~/.config/hypr
cp ./nvim ~/.config/nvim
cp ./ignis ~/.config/ignis
cp ./zsh/zshrc ~/.zshrc
cp ./zsh/oh-my-zsh ~/.oh-my-zsh

mkdir ~/Documents/swww-wallpapers
cp ./random_utils/auto-change-niri.sh ~/Documents/swww-wallpapers/

sudo pacman -Sy ruff ccls lua-language-server rust-analyzer vscode-html-languageserver
yay -S ltex-ls-plus-bin oh-my-zsh-git
