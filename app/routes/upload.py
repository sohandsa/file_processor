from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/rf",
    tags=["Robot Framework"],
)

@router.post("/")
async def output_loader(xmlFile: UploadFile):
    if xmlFile.content_type != "text/xml":
        return {"error": f"only xml content is accepted {xmlFile.content_type}"}
    return {"content_type": xmlFile.content_type}
