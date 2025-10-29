# Fix: Permission Name Standardization

## Problem Identified
The application was using inconsistent permission naming conventions:
- **Legacy format**: Underscore-based names like `'users_manage'`, `'inventory_view'`, `'inventory_manage'`, `'roles_manage'`
- **Standard format**: Dot-based names like `'users.view'`, `'inventory.view'`, `'inventory.edit'`, `'roles.view'`

This mismatch caused **access denial** even when users had the correct permissions loaded from their roles.

## Root Cause
When role permissions were loading correctly (showing `['users.view', 'users.create', ...]`), the permission checks were looking for non-existent permission names like `'users_manage'`, resulting in `False`.

## Changes Applied

### File: `controllers/main_controller.py`

#### 1. User Management Permissions
**Lines Fixed**: 254, 693, 699, 965, 1816

**Before**:
```python
if self.auth_controller.has_permission('users_manage'):
if not self._check_user_permission('users_manage'):
'permission': 'users_manage'
```

**After**:
```python
if self.auth_controller.has_permission('users.view'):
if not self._check_user_permission('users.view'):
'permission': 'users.view'
```

**Locations Changed**:
- **Line ~254**: Admin menu creation - Now checks `'users.view'`
- **Line ~693**: Module definition for Users - Now uses `'users.view'`
- **Line ~699**: Module permission property - Now uses `'users.view'`
- **Line ~965**: Administration button - Now checks `'users.view'`
- **Line ~1816**: `_manage_users()` method - Now checks `'users.view'`

#### 2. Role Management Permissions
**Line Fixed**: 1874

**Before**:
```python
if not self._check_user_permission('roles_manage'):
```

**After**:
```python
if not self._check_user_permission('roles.view'):
```

**Location Changed**:
- **Line ~1874**: `_manage_roles()` method - Now checks `'roles.view'`

#### 3. Inventory Permissions
**Lines Fixed**: 234, 240, 311, 320, 675, 681, 942

**Before**:
```python
if self.auth_controller.has_permission('inventory_view'):
if self.auth_controller.has_permission('inventory_manage'):
'permission': 'inventory_view'
```

**After**:
```python
if self.auth_controller.has_permission('inventory.view'):
if self.auth_controller.has_permission('inventory.edit'):
'permission': 'inventory.view'
```

**Locations Changed**:
- **Line ~234**: Inventory menu creation - Now checks `'inventory.view'`
- **Line ~240**: Inventory menu edit options - Now checks `'inventory.edit'` (changed from `inventory_manage`)
- **Line ~311**: Inventory button creation - Now checks `'inventory.view'`
- **Line ~320**: Inventory button edit options - Now checks `'inventory.edit'`
- **Line ~675**: Module definition for Products - Now checks `'inventory.view'`
- **Line ~681**: Module permission property - Now uses `'inventory.view'`
- **Line ~942**: Products button - Now checks `'inventory.view'`

## Standard Permission Format

All permissions now follow the **dot notation** format defined in `models/role_model.py`:

### Users Module
- `'users.view'` - View users list
- `'users.create'` - Create new users
- `'users.edit'` - Edit existing users
- `'users.delete'` - Delete users
- `'users.activate'` - Activate users
- `'users.deactivate'` - Deactivate users
- `'users.export'` - Export user data

### Roles Module
- `'roles.view'` - View roles list
- `'roles.create'` - Create new roles
- `'roles.edit'` - Edit existing roles
- `'roles.delete'` - Delete roles
- `'roles.assign'` - Assign roles to users
- `'roles.permissions'` - Manage role permissions

### Inventory Module
- `'inventory.view'` - View products/inventory
- `'inventory.create'` - Create new products
- `'inventory.edit'` - Edit existing products
- `'inventory.delete'` - Delete products
- `'inventory.stock'` - Manage stock levels
- `'inventory.reports'` - View inventory reports
- `'inventory.export'` - Export inventory data

### Reports Module
- `'reports.sales'` - Sales reports
- `'reports.inventory'` - Inventory reports
- `'reports.users'` - User reports
- `'reports.financial'` - Financial reports
- `'reports.export'` - Export reports

## Permissions Not Yet Standardized

The following legacy permissions are still in use and should be reviewed:

### Reports Permissions
- `'reports_basic'` - Used in lines 245, 326, 684, 690, 957
- `'reports_full'` - Used in lines 250, 333

**Note**: These permissions (`reports_basic`, `reports_full`) are **NOT defined** in `models/role_model.py`. 

**Recommendation**: Replace with standard permissions like `'reports.sales'` or create proper definitions in the role model if they represent aggregated permission sets.

## Impact of Changes

### ✅ Fixed Issues
1. **User Management Module**: Now accessible to users with `'users.view'` permission
2. **Role Management Module**: Now accessible to users with `'roles.view'` permission
3. **Inventory Module**: Now properly checks for `'inventory.view'` and `'inventory.edit'`
4. **Admin Menu**: Correctly shows/hides based on `'users.view'` permission
5. **Dashboard Modules**: Buttons and tiles show correctly based on standard permissions

### 🔍 What This Fixes
- Users with role `Test03` (containing `['users.view', 'users.create', ...]`) can now access user management
- Permission checks now match the permissions stored in the database
- No more "Acceso Denegado" errors for users with correct permissions

## Testing Checklist

To verify the fix:

1. **Login as user with custom role** (e.g., `testv4` with role `Test03`)
2. **Check admin menu visibility** - Should show if user has `'users.view'`
3. **Access User Management** - Should work without "Acceso Denegado" error
4. **Access Role Management** - Should work if user has `'roles.view'`
5. **Check inventory access** - Should work with `'inventory.view'`
6. **Monitor console logs**:
   ```
   DEBUG - Rol 'Test03' tiene 7 permisos
   🔍 Verificando permiso 'users.view': True  ✅ (Should be True now)
   ```

## Related Fixes

This fix builds upon previous work:
1. **Permission Loading** (FIX_PERMISSIONS_NOT_LOADING.md) - Ensured role permissions load correctly
2. **Permission Checking** (FIX_PERMISSIONS_NOT_LOADING.md) - Made permission checks null-safe
3. **User Update ENUM** (FIX_USER_TYPE_UPDATE_ERROR.md) - Fixed role to user_type mapping

## Technical Details

### Permission Check Flow
```
1. User logs in → prepare_user_data() loads role permissions
2. User data contains: {'permissions': ['users.view', 'users.create', ...]}
3. User clicks "Gestionar Usuarios"
4. _manage_users() calls _check_user_permission('users.view')  ✅ NOW MATCHES
5. Permission found in list → Access granted
```

### Before This Fix
```python
permissions = ['users.view', 'users.create', ...]  # Loaded correctly
_check_user_permission('users_manage')  # ❌ Looking for wrong name
# Result: False (permission not found)
```

### After This Fix
```python
permissions = ['users.view', 'users.create', ...]  # Loaded correctly
_check_user_permission('users.view')  # ✅ Looking for correct name
# Result: True (permission found!)
```

## Next Steps

### Immediate
1. ✅ **Test the application** - Login and verify all modules are accessible
2. ⏳ **Fix reports permissions** - Replace `reports_basic`/`reports_full` with standard permissions
3. ⏳ **Search other controllers** - Ensure no other files use legacy permission names

### Future Improvements
1. **Create permission constants** - Define all permission names in a single location
2. **Add permission validation** - Ensure only valid permission names are used
3. **Document permission hierarchy** - Create a comprehensive permission reference guide
4. **Remove debug logs** - Clean up excessive console output once verified

## Summary

**Total Changes**: ~15 permission name replacements across `controllers/main_controller.py`

**Modules Fixed**:
- ✅ Users Module (`users_manage` → `users.view`)
- ✅ Roles Module (`roles_manage` → `roles.view`)
- ✅ Inventory Module (`inventory_view/manage` → `inventory.view/edit`)

**Result**: Users with proper role permissions can now access their assigned modules without encountering "Acceso Denegado" errors.

---

**Created**: 2025-01-XX
**Author**: GitHub Copilot
**Related**: FIX_PERMISSIONS_NOT_LOADING.md, FIX_USER_TYPE_UPDATE_ERROR.md
