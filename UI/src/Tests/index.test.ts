import {describe, expect, it} from "vitest";
// Assuming handleMessage updates some visible text or state in the component
import {render} from "@testing-library/svelte";

describe("Math", () => {
  it("should add 2 + 2", () => {
    expect(2 + 2).toBe(4);
  });
});
