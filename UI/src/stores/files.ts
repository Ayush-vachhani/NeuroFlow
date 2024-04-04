import {writable} from "svelte/store";
import type {Writable} from "svelte/store";

export const files: Writable<string[]> = writable(null);

export const addFile = (file: string):void => {
    files.update((files:string[]) => [...files, file]);
}

export const removeFile = (file: string):void => {
    files.update((files:string[]) => files.filter(f => f !== file));
}

export const currentFile: Writable<string> = writable(null);

export const setCurrentFile = (file: string):void => {
    currentFile.set(file);
}