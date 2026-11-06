<cursor_untrusted_data_1337 source="CallDynamicTool">

const imgTextAlignRight = "https://www.figma.com/api/mcp/asset/3c8f8914-10c2-4fea-9de7-5f5298140915.svg";
const imgImage1 = "https://www.figma.com/api/mcp/asset/00d78215-e781-4497-8df1-1abcd3f8140d.png";
const imgCalling = "https://www.figma.com/api/mcp/asset/da30aa33-1301-44b2-b60d-5c6af840a210.svg";

function HiconOutlineTextAlignRight({ className }: { className?: string }) {
  return (
    <div className={className || "overflow-clip relative size-[24px]"} data-node-id="16:4516" data-name="Hicon / Outline / Text Align Right">
      <div className="absolute inset-[29.17%_18.75%_31.25%_16.67%]" data-node-id="16:4517" data-name="Text Align Right">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgTextAlignRight} />
      </div>
    </div>
  );
}

export default function Frame2() {
  return (
    <div className="bg-[rgba(38,38,38,0.2)] overflow-clip relative rounded-[20px] size-full" data-node-id="16:4507">
      <div className="-translate-y-1/2 absolute content-stretch flex items-center justify-between left-[12px] top-1/2 w-[339px]" data-node-id="16:4508">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="16:4509">
          <div className="h-[39px] relative shrink-0 w-[46px]" data-node-id="16:4510" data-name="image 1">
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <img alt="" className="absolute h-[106.84%] left-[-5.93%] max-w-none top-[-4.27%] w-[111.11%]" src={imgImage1} />
            </div>
          </div>
        </div>
        <div className="content-stretch flex gap-[20px] items-center justify-center relative shrink-0" data-node-id="16:4511">
          <div className="content-stretch flex gap-[8px] items-center justify-center relative shrink-0" data-node-id="16:4512">
            <div className="relative shrink-0 size-[18px]" data-node-id="16:4513" data-name="Iconly/Regular/Light/Calling">
              <div className="absolute inset-[10.42%_10.86%_10.42%_8.33%]" data-node-id="I16:4513;29221:1682" data-name="Calling">
                <div className="absolute inset-[-5.26%_-5.16%]">
                  <img alt="" className="block max-w-none size-full" src={imgCalling} />
                </div>
              </div>
            </div>
            <p className="[word-break:break-word] font-['Involve:SemiBold'] leading-[1.2] not-italic relative shrink-0 text-[12px] text-white whitespace-nowrap" data-node-id="16:4514">
              068 806 83 16
            </p>
          </div>
          <div className="bg-[#45db00] content-stretch flex items-center justify-center py-[14px] relative rounded-[12px] shrink-0 size-[44px]" data-node-id="16:4515">
            <HiconOutlineTextAlignRight className="overflow-clip relative shrink-0 size-[24px]" />
          </div>
        </div>
      </div>
    </div>
  );
}
SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.

Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.
The generated code contains image and SVG URL constants, e.g. const image = 'https://www.figma.com/api/mcp/asset/550e8400-e29b-41d4-a716-446655440000.png'. These URLs are temporary download sources and expire after 7 days. Download each asset into the project with curl -L, then replace its URL in the generated code with a reference to the downloaded asset. Never use the temporary URLs as runtime image sources.

</cursor_untrusted_data_1337>