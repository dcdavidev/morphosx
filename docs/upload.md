# Asset Upload Management in MorphosX

MorphosX allows file uploads via multipart POST. Assets can be either public (accessible via signature) or private (accessible only by the owner via signature).

## Upload Endpoint

- **URL**: `POST /assets/upload`
- **Body**: `multipart/form-data` with `file` field.
- **Query Parameters**:
  - `private` (bool, default=False): If set to `True`, the asset is saved in a folder specific to the logged-in user.
  - `folder` (string, optional): Subfolder where the asset should be saved.

## Public Workflow (Public Assets)

1.  **Request**: Send the file to the endpoint without parameters or with `private=False`.
2.  **Destination**: The asset is saved in `originals/{folder}/{uuid}.ext`.
3.  **Response**: Returns an `asset_id` (filename only) and a sample signed URL.

## Private Workflow (Private Assets)

1.  **Auth**: An authorization token (JWT) must be sent in the `Authorization: Bearer <token>` header.
2.  **Request**: Send the file with `private=True`.
3.  **Destination**: The asset is saved in `users/{user_id}/{folder}/{uuid}.ext`.
4.  **Response**: Returns a full `asset_id` (e.g., `users/123/file.jpg`) and a user-specific signed URL.

## cURL Example

### Public Upload
```bash
curl -X POST "http://localhost:8000/assets/upload?folder=avatar" \
     -F "file=@my_file.jpg"
```

### Private Upload
```bash
curl -X POST "http://localhost:8000/assets/upload?private=true" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -F "file=@confidential_document.pdf"
```
