<?php

namespace App\Http\Controllers;
use App\Models\Password;
use Illuminate\Http\Request;

class PasswordController extends Controller
{
    //

    public function index() {
        return response()->json(Password::all(), 200);
    }

    public function store(Request $request) {
        $password = Password::create($request->all());
        if (!$password) {
            return response()->json(['success' => false, 'message' => 'Gagal menyimpan password ke MySQL.'], 500);
        }
        return response()->json(['success' => true, 'message' => 'Password berhasil tersimpan ke MySQL.', 'data' => $password], 201);
    }

    public function update(Request $request, $id)
    {
        $password = Password::find($id);
        if (!$password) {
            return response()->json(['success' => false, 'message' => 'Data not found'], 404);
        }

        $password->update($request->all());
        
        return response()->json([
            'success' => true,
            'message' => 'Data updated successfully by Laravel!',
            'data' => $password
        ], 200);
    }

    public function destroy($id)
    {
        $password = Password::find($id);
        if (!$password) {
            return response()->json(['success' => false, 'message' => 'Data not found'], 404);
        }

        $password->delete();
        
        return response()->json([
            'success' => true,
            'message' => 'Data deleted successfully by Laravel!'
        ], 200);
    }
}
